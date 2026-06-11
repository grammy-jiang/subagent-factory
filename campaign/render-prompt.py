#!/usr/bin/env python3
"""Render a campaign prompt template (no LLM). Keeps fragile multi-line string
substitution out of the shell driver.

Usage: render-prompt.py TEMPLATE_PATH
Reads replacement values from the environment: any KEY in the template written
as ``{{KEY}}`` is replaced by ``os.environ[KEY]`` when set.
"""

from __future__ import annotations

import os
import re
import sys


def main() -> int:
    if len(sys.argv) < 2:
        print("usage: render-prompt.py TEMPLATE_PATH", file=sys.stderr)
        return 2
    text = open(sys.argv[1], encoding="utf-8").read()
    for key in set(re.findall(r"\{\{(\w+)\}\}", text)):
        text = text.replace("{{" + key + "}}", os.environ.get(key, ""))
    sys.stdout.write(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
