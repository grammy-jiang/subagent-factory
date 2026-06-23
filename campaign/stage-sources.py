#!/usr/bin/env python3
"""Stage source PDFs -> Markdown for dual-engine subagent authoring.

Fast converter: pymupdf4llm (keeps headings, no ML/Docling wait). Writes one .md per
book under campaign/staging/<slug>/ and a campaign/<slug>.sources list. Verifies each
output has >0 markdown headings (flat text => weak anchors => abort).
"""
from __future__ import annotations
import re, sys
from pathlib import Path

import pymupdf4llm

REPO = Path(__file__).resolve().parent.parent
PROJECTS = REPO.parent
BOOKS = PROJECTS / "awesome-book-collection"

SETS: dict[str, list[str]] = {
    "software-design": [
        "Software Architecture/A Philosophy of Software Design - John Ousterhout.pdf",
        "programming/clean-code/Code Simplicity -The Fundamentals of Software.pdf",
        "programming/clean-code/Clean Code_ A Handbook of Agile Software Craftsmanship - Robert C. Martin.pdf",
        "Software Engineering/Martin Fowler - Refactoring - Improving the Design of Existing Code.pdf",
        "programming/design-pattern/Erich Gamma, Richard Helm, Ralph Johnson, John M. Vlissides - Design Patterns_ Elements of Reusable Object-Oriented Software (1994, Addison-Wesley Professional) - libgen.li.pdf",
    ],
    "software-architecture": [
        "Software Architecture/Fundamentals of Software Architecture.pdf",
        "Software Architecture/Book - Clean Architecture - Robert Cecil Martin.pdf",
        "Software Architecture/Software Architecture The Hard Parts - Neal Ford, Mark Richards, Pramod Sadalage, Zhamak Dehghani.pdf",
        "Software Architecture/Patterns of Enterprise Application Architecture.pdf",
        "Software Architecture/Mark Richards - Software Architecture Patterns (2015, O'Reilly).pdf",
        "Software Architecture/Designing_Event_Driven_Systems.pdf",
        "Software Architecture/Enterprise Integration Patterns_ Designing, Building, and Deploying Messaging Solutions  -Addison-Wesley Professional (2003).pdf",
    ],
    "python-code-reviewer": [
        "programming/python/Luciano Ramalho - Fluent Python_ Clear, Concise, and Effective Programming-O'Reilly Media (2022).pdf",
        "programming/python/Python Distilled - Pearson (2021) - David Beazley.pdf",
    ],
    "devops-sre-advisor": [
        "devops/The DevOps Handbook_ How to Create World-Class Agility, Reliability, & Security in Technology Organizations-Gene Kim, Jez Humble, Patrick Debois, John Willis, Nicole Forsgren.pdf",
        "Software Architecture/Accelerate_ The Science of DevOps ( PDFDrive ).pdf",
        "devops/cicd/Pipeline as Code_ Continuous Delivery with Jenkins, Kubernetes, and Terraform-Manning (2021) - Mohamed Labouardy.pdf",
        "Computer-Science-Reference-Books/comp(500).pdf",
        "Computer-Science-Reference-Books/comp(109).pdf",
    ],
}

def slugify(name: str) -> str:
    s = re.sub(r"\.pdf$", "", name, flags=re.I)
    s = re.sub(r"[_\s]+", "-", s.strip().lower())
    s = re.sub(r"[^a-z0-9-]", "", s)
    return re.sub(r"-+", "-", s).strip("-")[:60]

def heading_count(md: str) -> int:
    return sum(1 for ln in md.splitlines() if re.match(r"#{1,6}\s+\S", ln))

def main() -> int:
    only = set(sys.argv[1:])
    rc = 0
    for slug, rels in SETS.items():
        if only and slug not in only:
            continue
        out_dir = REPO / "campaign" / "staging" / slug
        out_dir.mkdir(parents=True, exist_ok=True)
        staged: list[Path] = []
        print(f"\n=== {slug} ===")
        for rel in rels:
            # Relative paths resolve against BOOKS (awesome-book-collection) first, then the PROJECTS
            # root, so sibling corpora are referenced portably without a machine-specific /home/ path.
            if rel.startswith("/"):
                src = Path(rel)
            else:
                src = BOOKS / rel
                if not src.is_file():
                    src = PROJECTS / rel
            if not src.is_file():
                print(f"  MISSING: {src}"); rc = 1; continue
            short = slugify(Path(rel).name)
            dst = out_dir / f"{short}.md"
            try:
                md = pymupdf4llm.to_markdown(str(src))
            except Exception as e:
                print(f"  FAILED  {short}: {e}"); rc = 1; continue
            hc = heading_count(md)
            dst.write_text(md, encoding="utf-8")
            staged.append(dst)
            flag = "" if hc > 0 else "  <-- WARN: 0 headings (flat)"
            print(f"  ok  {short}.md  ({len(md):>8} chars, {hc:>4} headings){flag}")
            if hc == 0:
                rc = 1
        sources_file = REPO / "campaign" / f"{slug}.sources"
        sources_file.write_text("".join(f"{p}\n" for p in staged), encoding="utf-8")
        print(f"  -> wrote {sources_file.relative_to(REPO)} ({len(staged)} sources)")
    return rc

if __name__ == "__main__":
    raise SystemExit(main())
