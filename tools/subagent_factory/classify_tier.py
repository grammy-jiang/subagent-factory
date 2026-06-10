"""Deterministic tier classification (enhancement Step 0).

Tier governs which enhancement artifacts a package must carry (see
``docs/enhancement-steps/step-0-plumbing.md`` and the build plan §7):

  Tier 0 — single short source (the current default for all existing packages).
  Tier 1 — long / content-dense source(s).
  Tier 2 — multiple high-value sources.

Thresholds are provisional; calibrate over the corpus before relying on Tier-1
promotion. This module is **pure computation** — it does not mutate any package.
Existing packages carry no ``tier:`` field and therefore read as Tier 0 (see
``validate_generated_package._tier``), so nothing here changes their behaviour.
"""

import sys
from pathlib import Path

import yaml

TIER1_MIN_WORDS = 15000


def _manifest_source_count(base: Path) -> int:
    mp = base / "source-pack.manifest.yaml"
    if not mp.exists():
        return 0
    try:
        manifest = yaml.safe_load(mp.read_text(encoding="utf-8")) or {}
    except yaml.YAMLError:
        return 0
    return len(manifest.get("sources", []) or [])


def _total_source_words(base: Path) -> int:
    md_dir = base / "sources" / "markdown"
    if not md_dir.exists():
        return 0
    total = 0
    for p in md_dir.glob("*.md"):
        try:
            total += len(p.read_text(encoding="utf-8").split())
        except OSError:
            continue
    return total


def classify_tier(base: str | Path) -> int:
    """Return the suggested tier (0/1/2) for a package. Pure; does not write."""
    base = Path(base)
    if _manifest_source_count(base) >= 2:
        return 2
    if _total_source_words(base) >= TIER1_MIN_WORDS:
        return 1
    return 0


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: python -m tools.subagent_factory.classify_tier subagents/<slug>")
        sys.exit(1)
    print(classify_tier(sys.argv[1]))


if __name__ == "__main__":
    main()
