#!/usr/bin/env python3
"""Run the full package validator over the affected subagent package(s).

Used by three callers:

* pre-push hook  — `validate_subagents.py <staged files...>` (pass_filenames)
* CI / make      — `validate_subagents.py --range origin/master`
* make           — `validate_subagents.py --all`

It derives the unique set of slugs touched, runs `cli validate <slug>` for
each (the authoritative gate: profile, claims, evidence, principles, skills,
adapter policy, faithfulness, quote-scan, ...), and exits non-zero if any
package fails. `cli validate` rewrites tests/test-results.md as a side effect;
this restores that file when it is tracked so the run leaves no spurious diff.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

SUBAGENTS = "subagents"
BACKUP_DIR = ".backups"
ADAPTER_DIR = ".claude/agents/generated"


def repo_root() -> Path:
    out = subprocess.run(
        ["git", "rev-parse", "--show-toplevel"],
        capture_output=True,
        text=True,
        check=True,
    )
    return Path(out.stdout.strip())


def slug_of(path: str) -> str | None:
    """`subagents/<slug>/...` -> `<slug>`; otherwise None. Skips .backups."""
    parts = Path(path).parts
    if len(parts) < 2 or parts[0] != SUBAGENTS:
        return None
    slug = parts[1]
    if slug == BACKUP_DIR or slug.startswith("."):
        return None
    return slug


def slugs_from_files(files: list[str]) -> set[str]:
    return {s for f in files if (s := slug_of(f))}


def slugs_from_range(base: str, root: Path) -> set[str]:
    rng = f"{base}...HEAD" if base else "HEAD"
    out = subprocess.run(
        ["git", "diff", "--name-only", rng],
        capture_output=True,
        text=True,
        cwd=root,
        check=True,
    )
    return slugs_from_files(out.stdout.splitlines())


def slugs_all(root: Path) -> set[str]:
    return {
        p.parent.name
        for p in (root / SUBAGENTS).glob("*/profile.yaml")
        if p.parent.name != BACKUP_DIR
    }


def is_tracked(path: Path, root: Path) -> bool:
    return (
        subprocess.run(
            ["git", "ls-files", "--error-unmatch", str(path)],
            cwd=root,
            capture_output=True,
        ).returncode
        == 0
    )


def orphan_adapters(root: Path) -> list[str]:
    """Installed adapters that have no canonical ``subagents/<slug>/profile.yaml``.

    Repo-level, not per-package: ``cli validate <slug>`` is invoked per package, so a package
    that does not exist is never validated and its leftover adapter stays invisible to every
    gate while remaining loadable by the runtime. That inverts the repository rule that
    profile.yaml is canonical and the adapter is derived.

    Found 2026-07-25: 14 adapters had outlived their packages — 8 whose packages existed only on
    an unmerged local branch (deleting it would have made 8 working agents unreproducible) and 6
    whose packages were on no ref at all. Nothing in CI could see any of them.

    Checks the working tree, which in CI is the committed state — so CI catches a committed
    adapter whose package was never committed, and the pre-push hook additionally catches an
    untracked local one.
    """
    adapters = root / ADAPTER_DIR
    if not adapters.is_dir():
        return []
    return sorted(
        md.stem
        for md in adapters.glob("*.md")
        if md.stem != "README" and not (root / SUBAGENTS / md.stem / "profile.yaml").is_file()
    )


def validate_one(slug: str, root: Path) -> int:
    """Run `cli validate <slug>`; restore test-results.md if it got dirtied."""
    pkg = root / SUBAGENTS / slug
    if not (pkg / "profile.yaml").is_file():
        # Package deleted in this change set — nothing to validate.
        print(f"[skip] {slug}: no profile.yaml (deleted?)")
        return 0

    results = pkg / "tests" / "test-results.md"
    tracked = results.is_file() and is_tracked(results, root)

    print(f"[validate] {slug}")
    rc = subprocess.run(
        [sys.executable, "-m", "tools.subagent_factory.cli", "validate", slug],
        cwd=root,
    ).returncode

    if tracked:  # undo the validator's write so the tree stays clean
        subprocess.run(
            ["git", "checkout", "--quiet", "--", str(results)],
            cwd=root,
        )
    return rc


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    g = ap.add_mutually_exclusive_group()
    g.add_argument("--range", metavar="BASE", help="validate slugs changed in BASE...HEAD")
    g.add_argument("--all", action="store_true", help="validate every tracked package")
    ap.add_argument("files", nargs="*", help="staged files (pre-push pass_filenames)")
    args = ap.parse_args(argv)

    root = repo_root()

    # Repo-level invariant, checked on EVERY invocation — deliberately before the
    # "no packages changed" early return below, since an orphan adapter is exactly the case
    # where no package changed and so nothing else would look.
    if orphans := orphan_adapters(root):
        print(
            f"ADAPTER/PACKAGE MISMATCH: {len(orphans)} installed adapter(s) have no canonical "
            f"package: {', '.join(orphans)}",
            file=sys.stderr,
        )
        print(
            "Each .claude/agents/generated/<slug>.md requires subagents/<slug>/profile.yaml "
            "(profile.yaml is canonical; the adapter is derived). Commit the package, or remove "
            "the adapter.",
            file=sys.stderr,
        )
        return 1

    if args.all:
        slugs = slugs_all(root)
    elif args.range:
        slugs = slugs_from_range(args.range, root)
    else:
        slugs = slugs_from_files(args.files)

    if not slugs:
        print("No subagent package changes to validate.")
        return 0

    failed: list[str] = []
    for slug in sorted(slugs):
        if validate_one(slug, root) != 0:
            failed.append(slug)

    print()
    if failed:
        print(f"PACKAGE VALIDATION FAILED: {', '.join(failed)}", file=sys.stderr)
        print("Emergency bypass (discouraged): git push --no-verify", file=sys.stderr)
        return 1
    print(f"Package validation passed: {', '.join(sorted(slugs))}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
