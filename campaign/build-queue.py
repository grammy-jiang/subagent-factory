#!/usr/bin/env python3
"""Build / refresh the campaign PDF queue (deterministic; no LLM).

Walks the book collection, sorts PDFs by size (a length/complexity proxy), and
marks each as ``done`` when its sha256 already appears in a generated package
(``subagents/*/source-pack.manifest.yaml``) **and that package validates** — so
already-authored sources are skipped, while a package left incomplete by an
interrupted run (e.g. usage-limit) stays ``pending`` for a repair round.
Idempotent: terminal statuses (done/blocked/error/review) recorded by
run.sh in a prior queue are preserved, and unchanged files reuse their cached
sha256 instead of being re-hashed.

Outputs (both gitignored):
  campaign/pdf-queue.tsv     machine source of truth
  campaign/pdf-inventory.md  human-readable view

Usage: build-queue.py [COLLECTION_DIR]
"""

from __future__ import annotations

import csv
import hashlib
import sys
from datetime import date
from pathlib import Path
from typing import Any

import yaml

REPO = Path(__file__).resolve().parent.parent
CAMPAIGN = REPO / "campaign"
QUEUE = CAMPAIGN / "pdf-queue.tsv"
INVENTORY = CAMPAIGN / "pdf-inventory.md"
SUBAGENTS = REPO / "subagents"
DEFAULT_COLLECTION = Path.home() / "projects" / "awesome-book-collection"
TERMINAL = {"done", "blocked", "error", "review"}
HEADER = ["idx", "size_bytes", "status", "slug", "sha256", "relpath"]

# Make the factory's deterministic validators importable (campaign/ sits outside the
# tools package) so `_package_valid` can confirm a sha-matched package is complete.
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def manifest_shas() -> dict[str, str]:
    """Map sha256 -> slug for every source already ingested into a package."""
    out: dict[str, str] = {}
    if not SUBAGENTS.exists():
        return out
    for manifest in SUBAGENTS.glob("*/source-pack.manifest.yaml"):
        slug = manifest.parent.name
        try:
            data = yaml.safe_load(manifest.read_text(encoding="utf-8")) or {}
        except Exception:
            continue
        for src in data.get("sources", []) or []:
            sha = src.get("sha256")
            if sha:
                out[sha] = slug
    return out


def load_prior() -> dict[str, dict[str, str]]:
    """Existing queue rows keyed by relpath (to reuse sha + preserve status)."""
    prior: dict[str, dict[str, str]] = {}
    if not QUEUE.exists():
        return prior
    with open(QUEUE, newline="", encoding="utf-8") as fh:
        for row in csv.DictReader(fh, delimiter="\t"):
            prior[row["relpath"]] = row
    return prior


def _package_valid(slug: str) -> bool:
    """True only if the generated package actually passes validation.

    A sha match alone is insufficient: a run interrupted (e.g. usage-limit) after
    ingesting the source but before finishing leaves a package whose sha is already
    in the manifest yet whose package is incomplete/invalid. Such a PDF must stay
    pending so a later round repairs it — not be silently marked done.
    """
    pkg = SUBAGENTS / slug
    if not pkg.exists():
        return False
    try:
        from tools.subagent_factory.validate_generated_package import (
            validate_generated_package,
        )

        return bool(validate_generated_package(pkg).get("passed"))
    except Exception:
        return False


def build(collection: Path) -> list[dict[str, Any]]:
    shas = manifest_shas()
    prior = load_prior()
    rows: list[dict[str, Any]] = []
    for p in collection.rglob("*.pdf"):
        size = p.stat().st_size
        rel = str(p.relative_to(collection))
        pr = prior.get(rel)
        # Reuse cached sha256 when the file is unchanged (same size).
        if pr and pr.get("sha256") and pr.get("size_bytes") == str(size):
            sha = pr["sha256"]
        else:
            sha = sha256_file(p)
        slug, status = "", "pending"
        if sha in shas:
            # A sha in a manifest means the source was ingested — but an interrupted
            # run (e.g. usage-limit) can leave the package incomplete. Mark done only
            # if it actually validates; otherwise keep it pending for a repair round.
            slug = shas[sha]
            status = "done" if _package_valid(slug) else "pending"
        elif pr and pr.get("status") in TERMINAL:
            slug, status = pr.get("slug", ""), pr["status"]
        rows.append({"size": size, "status": status, "slug": slug, "sha256": sha, "relpath": rel})
    rows.sort(key=lambda r: (r["size"], r["relpath"]))
    return rows


def write_queue(rows: list[dict[str, Any]]) -> None:
    QUEUE.parent.mkdir(parents=True, exist_ok=True)
    with open(QUEUE, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh, delimiter="\t", lineterminator="\n")
        w.writerow(HEADER)
        for i, r in enumerate(rows, 1):
            w.writerow([i, r["size"], r["status"], r["slug"], r["sha256"], r["relpath"]])


def write_inventory(rows: list[dict[str, Any]], collection: Path) -> None:
    done = sum(1 for r in rows if r["status"] == "done")
    pend = sum(1 for r in rows if r["status"] == "pending")
    other = len(rows) - done - pend
    lines = [
        f"# PDF Inventory — {collection.name}",
        "",
        f"Generated {date.today()} · {len(rows)} PDFs · {done} done · {pend} pending · "
        f"{other} blocked/error/review · sorted smallest→largest (size = complexity proxy).",
        "",
        "| # | Size (KB) | Status | Slug | Path |",
        "|--:|----------:|:-------|:-----|:-----|",
    ]
    for i, r in enumerate(rows, 1):
        rel_esc = r["relpath"].replace("|", "\\|")
        lines.append(f"| {i} | {r['size'] // 1024} | {r['status']} | {r['slug']} | {rel_esc} |")
    INVENTORY.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    collection = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_COLLECTION
    if not collection.is_dir():
        print(f"collection not found: {collection}", file=sys.stderr)
        return 2
    rows = build(collection)
    write_queue(rows)
    write_inventory(rows, collection)
    done = sum(1 for r in rows if r["status"] == "done")
    pend = sum(1 for r in rows if r["status"] == "pending")
    print(f"queue: {len(rows)} PDFs · {done} done · {pend} pending -> {QUEUE}")
    for i, r in enumerate(rows, 1):
        if r["status"] == "pending":
            print(f"next_pending: #{i} ({r['size'] // 1024} KB) {r['relpath']}")
            break
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
