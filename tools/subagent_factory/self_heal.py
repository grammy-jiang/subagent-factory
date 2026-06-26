"""Self-healing dependency management for the subagent factory.

When a factory script needs an optional converter package that is not installed,
this module installs it on demand and retries the import — so a PDF/ePUB/DOCX
ingest "just works" without a manual `pip install` first.

Design and safety:
- **Allowlist only.** Auto-install is restricted to a fixed set of known
  converter / runtime packages (`ALLOWED_PACKAGES`). An import name that is not
  on the allowlist is never installed — `ensure_package` returns ``None`` and the
  caller falls back or reports the missing dependency.
- **Opt-out.** Set ``SUBAGENT_FACTORY_NO_AUTOINSTALL=1`` to disable all
  auto-install; ``ensure_package`` then only imports what is already present.
- **Current interpreter.** In-process healing installs into ``sys.executable`` so
  the retry import in the same process can succeed.
- **Managed venv (opt-in).** ``bootstrap_environment`` creates a project ``.venv``
  and installs the ``convert`` extra; ``ensure_environment`` re-execs the CLI into
  that venv when ``SUBAGENT_FACTORY_USE_VENV=1``.
- Every install is logged to stderr.

System binaries (e.g. ``pandoc``) are detected but never auto-installed —
``ensure_system_tool`` reports an actionable hint instead.
"""

from __future__ import annotations

import importlib
import os
import shutil
import subprocess
import sys
from pathlib import Path
from types import ModuleType

# import name -> pip requirement spec. Only these may be auto-installed.
ALLOWED_PACKAGES: dict[str, str] = {
    # converters (light, self-heal default)
    "markitdown": "markitdown[pdf]>=0.1.0",
    "readability": "readability-lxml>=0.8",
    "markdownify": "markdownify>=0.12",
    "bs4": "beautifulsoup4>=4.12",
    # runtime stack
    "slugify": "python-slugify>=8.0",
    "yaml": "pyyaml>=6.0",
    "jsonschema": "jsonschema>=4.0",
    "jinja2": "jinja2>=3.1",
    "rich": "rich>=13.0",
    "pydantic": "pydantic>=2.0",
    "requests": "requests>=2.31",
    "click": "click>=8.1",
    # OCR / optional
    "fitz": "pymupdf>=1.23",
}

# System tools the factory can use, with how to obtain them. Never auto-installed.
SYSTEM_TOOLS: dict[str, str] = {
    "pandoc": "Install Pandoc (https://pandoc.org/installing.html) — e.g. `dnf install pandoc` / `brew install pandoc`. The MarkItDown fallback covers ePUB/DOCX without it.",
    "tesseract": "Install Tesseract OCR for scanned PDFs — e.g. `dnf install tesseract` / `brew install tesseract`.",
}

_REPO_ROOT = Path(__file__).resolve().parent.parent.parent
_VENV_DIR = _REPO_ROOT / ".venv"

# Per-process memo so we attempt each install at most once.
_install_attempted: set[str] = set()


def _log(msg: str) -> None:
    print(f"[self-heal] {msg}", file=sys.stderr, flush=True)


def autoinstall_enabled() -> bool:
    return os.environ.get("SUBAGENT_FACTORY_NO_AUTOINSTALL", "") not in ("1", "true", "yes")


# Subprocess wall-clock budget (seconds) for any pip/uv install.
_INSTALL_TIMEOUT = 600

# Wall-clock budget (seconds) for the post-install import probe. A bare `import`
# that has not returned in seconds is wedged (corrupt install deadlocking the
# loader, a converter blocking on a network/device probe at import time), not
# slow — so it gets its own short budget instead of sharing the 10-minute
# install timeout, which would otherwise stall bootstrap silently.
_IMPORT_PROBE_TIMEOUT = 60


def _install_cmd(target: str, python: str) -> list[str]:
    """Build the install command for ``target`` against interpreter ``python``.

    Uses ``uv pip install --python <python>`` when ``uv`` is on PATH, else
    ``<python> -m pip install``. Single source of truth for the three install
    sites (in-process heal + venv create-and-install).
    """
    if shutil.which("uv"):
        return ["uv", "pip", "install", "--python", python, target]
    return [python, "-m", "pip", "install", target]


def _run_install(cmd: list[str], target: str, *, cwd: str | None = None) -> tuple[bool, str]:
    """Run an install ``cmd``. Returns (ok, error_detail).

    Enforces ``_INSTALL_TIMEOUT`` so a wedged installer cannot hang the process.
    """
    _log(f"installing {target} via: {' '.join(cmd)}")
    try:
        proc = subprocess.run(
            cmd, capture_output=True, text=True, timeout=_INSTALL_TIMEOUT, cwd=cwd
        )
    except subprocess.TimeoutExpired:
        msg = f"install timed out after {_INSTALL_TIMEOUT}s: {target}"
        _log(msg)
        return False, msg
    except Exception as e:  # pragma: no cover - defensive
        msg = f"install error for {target}: {e}"
        _log(msg)
        return False, msg
    if proc.returncode != 0:
        detail = (proc.stderr or proc.stdout or "").strip()
        tail = detail.splitlines()[-3:]
        _log(f"install failed for {target} (exit {proc.returncode}): {' | '.join(tail)}")
        return False, detail[:300]
    _log(f"installed {target}")
    return True, ""


def _pip_install(spec: str) -> bool:
    """Install ``spec`` into the current interpreter. Returns True on success."""
    ok, _ = _run_install(_install_cmd(spec, sys.executable), spec)
    return ok


def ensure_package(import_name: str, *, purpose: str = "") -> ModuleType | None:
    """Import ``import_name``, auto-installing it first if necessary and allowed.

    Returns the imported module, or ``None`` if it is unavailable and cannot be
    healed (not on the allowlist, auto-install disabled, or install failed).
    """
    try:
        return importlib.import_module(import_name)
    except ImportError:
        pass

    spec = ALLOWED_PACKAGES.get(import_name)
    if spec is None:
        _log(f"'{import_name}' is not on the auto-install allowlist; not installing")
        return None
    if not autoinstall_enabled():
        _log(f"'{import_name}' missing and auto-install disabled (SUBAGENT_FACTORY_NO_AUTOINSTALL)")
        return None
    if spec in _install_attempted:
        return None
    _install_attempted.add(spec)

    why = f" (needed for {purpose})" if purpose else ""
    _log(f"'{import_name}' missing{why} — attempting install")
    if not _pip_install(spec):
        return None
    importlib.invalidate_caches()
    try:
        return importlib.import_module(import_name)
    except ImportError as e:
        _log(f"still cannot import '{import_name}' after install: {e}")
        return None


def ensure_system_tool(name: str) -> tuple[bool, str]:
    """Check for a system binary. Returns (present, hint).

    Never auto-installs — system package managers vary and require privilege.
    """
    if shutil.which(name):
        return True, ""
    hint = SYSTEM_TOOLS.get(name, f"Install '{name}' and ensure it is on PATH.")
    return False, hint


def ensure_converter_stack(*, quiet: bool = False) -> dict:
    """Best-effort: ensure the light converter stack is importable.

    Heals MarkItDown (covers PDF/ePUB/DOCX). Reports system-tool availability.
    """
    report: dict = {"healed": [], "missing": [], "system_tools": {}}
    mod = ensure_package("markitdown", purpose="document conversion")
    if mod is None:
        report["missing"].append("markitdown")
    else:
        report["healed"].append("markitdown")
    for tool in ("pandoc",):
        present, hint = ensure_system_tool(tool)
        report["system_tools"][tool] = {"present": present, "hint": hint}
    if not quiet and report["missing"]:
        _log(f"converter stack still missing: {', '.join(report['missing'])}")
    return report


def doctor() -> dict:
    """Report converter dependency health without installing anything."""
    report: dict = {
        "python_packages": {},
        "system_tools": {},
        "venv": str(_VENV_DIR) if _VENV_DIR.exists() else None,
    }
    for name in ("markitdown", "readability", "markdownify", "bs4", "yaml", "jinja2", "fitz"):
        try:
            importlib.import_module(name)
            report["python_packages"][name] = True
        except ImportError:
            report["python_packages"][name] = False
    for tool in SYSTEM_TOOLS:
        present, hint = ensure_system_tool(tool)
        report["system_tools"][tool] = {"present": present, "hint": hint}
    return report


def _venv_python() -> Path:
    if os.name == "nt":  # pragma: no cover
        return _VENV_DIR / "Scripts" / "python.exe"
    return _VENV_DIR / "bin" / "python"


# Import name that must be loadable in the venv after the convert extra installs.
# Both `convert` and `convert-full` extras pull in markitdown (see pyproject.toml).
_VENV_VERIFY_IMPORT = "markitdown"


def _verify_venv_import(venv_python: str, import_name: str) -> bool:
    """Confirm ``import_name`` actually imports under the venv interpreter.

    Mirrors ``ensure_package``'s retry-import check: a zero exit code from the
    installer does not prove the package is importable, so probe it directly.
    """
    cmd = [venv_python, "-c", f"import {import_name}"]
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=_IMPORT_PROBE_TIMEOUT)
    except subprocess.TimeoutExpired:
        _log(f"import check timed out after {_IMPORT_PROBE_TIMEOUT}s: {import_name}")
        return False
    except Exception as e:  # pragma: no cover - defensive
        _log(f"import check error for {import_name}: {e}")
        return False
    if proc.returncode != 0:
        tail = (proc.stderr or proc.stdout or "").strip().splitlines()[-3:]
        _log(f"import check failed for {import_name}: {' | '.join(tail)}")
        return False
    return True


def bootstrap_environment(extra: str = "convert") -> dict:
    """Create the project ``.venv`` and install ``.[extra]`` into it.

    Returns a status dict. Used by ``cli bootstrap --venv``. ``installed`` is only
    True once the converter package is confirmed importable under the venv
    interpreter — a zero install exit code with a broken import reports failure.
    """
    result = {"venv": str(_VENV_DIR), "created": False, "installed": False, "error": None}
    venv_python = str(_venv_python())
    if not _VENV_DIR.exists():
        if shutil.which("uv"):
            cmd = ["uv", "venv", str(_VENV_DIR)]
        else:
            cmd = [sys.executable, "-m", "venv", str(_VENV_DIR)]
        _log(f"creating venv: {' '.join(cmd)}")
        try:
            proc = subprocess.run(cmd, capture_output=True, text=True, timeout=_INSTALL_TIMEOUT)
        except subprocess.TimeoutExpired:
            result["error"] = f"venv creation timed out after {_INSTALL_TIMEOUT}s"
            return result
        if proc.returncode != 0:
            result["error"] = f"venv creation failed: {(proc.stderr or proc.stdout).strip()[:300]}"
            return result
        result["created"] = True
    target = f".[{extra}]"
    ok, detail = _run_install(_install_cmd(target, venv_python), target, cwd=str(_REPO_ROOT))
    if not ok:
        result["error"] = f"install failed: {detail}"
        return result
    if not _verify_venv_import(venv_python, _VENV_VERIFY_IMPORT):
        result["error"] = (
            f"install reported success but '{_VENV_VERIFY_IMPORT}' is not importable "
            f"under {venv_python}"
        )
        return result
    result["installed"] = True
    return result


def ensure_environment() -> None:
    """Opt-in: re-exec the CLI inside the project ``.venv``.

    Active only when ``SUBAGENT_FACTORY_USE_VENV=1``. Guards against re-exec loops
    via ``SUBAGENT_FACTORY_BOOTSTRAPPED``. When disabled (default), this is a
    no-op and the lazy ``ensure_package`` path handles healing in-process.
    """
    if os.environ.get("SUBAGENT_FACTORY_USE_VENV", "") not in ("1", "true", "yes"):
        return
    if os.environ.get("SUBAGENT_FACTORY_BOOTSTRAPPED") == "1":
        return
    venv_py = _venv_python()
    if not venv_py.exists():
        status = bootstrap_environment()
        if status.get("error"):
            _log(f"venv bootstrap failed; continuing in current interpreter: {status['error']}")
            return
    # Already running inside the venv?
    try:
        if Path(sys.executable).resolve() == venv_py.resolve():
            return
    except OSError:  # pragma: no cover
        return
    env = dict(os.environ, SUBAGENT_FACTORY_BOOTSTRAPPED="1")
    _log(f"re-executing inside venv: {venv_py}")
    # Intentional re-exec into the project-managed venv interpreter.
    os.execve(str(venv_py), [str(venv_py), "-m", "tools.subagent_factory.cli", *sys.argv[1:]], env)  # nosec B606
