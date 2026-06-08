"""Tests for self-healing dependency management."""

import types

import tools.subagent_factory.self_heal as sh


def test_present_package_imports_without_install(monkeypatch):
    called = []
    monkeypatch.setattr(sh, "_pip_install", lambda spec: called.append(spec) or True)
    mod = sh.ensure_package("yaml")  # pyyaml is a declared core dep
    assert mod is not None and mod.__name__ == "yaml"
    assert called == []  # already importable, no install attempted


def test_unknown_package_is_refused_not_installed(monkeypatch):
    called = []
    monkeypatch.setattr(sh, "_pip_install", lambda spec: called.append(spec) or True)
    assert sh.ensure_package("totally_unknown_pkg_xyz") is None
    assert called == []  # never install something off the allowlist


def test_optout_blocks_install(monkeypatch):
    monkeypatch.setenv("SUBAGENT_FACTORY_NO_AUTOINSTALL", "1")
    sh._install_attempted.clear()
    called = []
    monkeypatch.setattr(sh, "_pip_install", lambda spec: called.append(spec) or True)
    monkeypatch.setattr(sh.importlib, "import_module",
                        lambda n: (_ for _ in ()).throw(ImportError()))
    assert sh.ensure_package("markitdown") is None
    assert called == []


def test_missing_allowlisted_package_installs_then_imports(monkeypatch):
    monkeypatch.delenv("SUBAGENT_FACTORY_NO_AUTOINSTALL", raising=False)
    sh._install_attempted.clear()
    state = {"installed": False, "spec": None}

    def fake_import(name):
        if name == "markitdown":
            if not state["installed"]:
                raise ImportError("missing")
            return types.ModuleType("markitdown")
        raise ImportError(name)

    def fake_pip(spec):
        state["installed"] = True
        state["spec"] = spec
        return True

    monkeypatch.setattr(sh.importlib, "import_module", fake_import)
    monkeypatch.setattr(sh, "_pip_install", fake_pip)
    mod = sh.ensure_package("markitdown", purpose="unit test")
    assert mod is not None
    assert state["spec"] == sh.ALLOWED_PACKAGES["markitdown"]


def test_failed_install_returns_none(monkeypatch):
    monkeypatch.delenv("SUBAGENT_FACTORY_NO_AUTOINSTALL", raising=False)
    sh._install_attempted.clear()
    monkeypatch.setattr(sh.importlib, "import_module",
                        lambda n: (_ for _ in ()).throw(ImportError()))
    monkeypatch.setattr(sh, "_pip_install", lambda spec: False)
    assert sh.ensure_package("markitdown") is None


def test_install_attempted_once_per_process(monkeypatch):
    monkeypatch.delenv("SUBAGENT_FACTORY_NO_AUTOINSTALL", raising=False)
    sh._install_attempted.clear()
    calls = []
    monkeypatch.setattr(sh.importlib, "import_module",
                        lambda n: (_ for _ in ()).throw(ImportError()))
    monkeypatch.setattr(sh, "_pip_install", lambda spec: calls.append(spec) or False)
    sh.ensure_package("markitdown")
    sh.ensure_package("markitdown")
    assert len(calls) == 1  # second call short-circuits on the memo


def test_ensure_system_tool_present_and_absent():
    present, hint = sh.ensure_system_tool("sh")
    assert present is True and hint == ""
    missing, hint2 = sh.ensure_system_tool("definitely_missing_tool_zzz")
    assert missing is False and hint2


def test_allowlist_specs_are_sane():
    assert "markitdown[pdf]" in sh.ALLOWED_PACKAGES["markitdown"]
    assert sh.ALLOWED_PACKAGES["readability"].startswith("readability-lxml")
    assert sh.ALLOWED_PACKAGES["slugify"].startswith("python-slugify")


def test_doctor_reports_without_installing(monkeypatch):
    called = []
    monkeypatch.setattr(sh, "_pip_install", lambda spec: called.append(spec) or True)
    report = sh.doctor()
    assert "python_packages" in report and "system_tools" in report
    assert "pandoc" in report["system_tools"]
    assert called == []  # doctor never installs
