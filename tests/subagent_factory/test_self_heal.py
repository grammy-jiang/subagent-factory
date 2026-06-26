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
    monkeypatch.setattr(
        sh.importlib, "import_module", lambda n: (_ for _ in ()).throw(ImportError())
    )
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
    monkeypatch.setattr(
        sh.importlib, "import_module", lambda n: (_ for _ in ()).throw(ImportError())
    )
    monkeypatch.setattr(sh, "_pip_install", lambda spec: False)
    assert sh.ensure_package("markitdown") is None


def test_install_attempted_once_per_process(monkeypatch):
    monkeypatch.delenv("SUBAGENT_FACTORY_NO_AUTOINSTALL", raising=False)
    sh._install_attempted.clear()
    calls = []
    monkeypatch.setattr(
        sh.importlib, "import_module", lambda n: (_ for _ in ()).throw(ImportError())
    )
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


def _fake_completed(returncode, stdout="", stderr=""):
    return types.SimpleNamespace(returncode=returncode, stdout=stdout, stderr=stderr)


def test_install_cmd_uses_uv_when_present(monkeypatch):
    monkeypatch.setattr(sh.shutil, "which", lambda name: "/usr/bin/uv")
    cmd = sh._install_cmd(".[convert]", "/venv/bin/python")
    assert cmd == ["uv", "pip", "install", "--python", "/venv/bin/python", ".[convert]"]


def test_install_cmd_falls_back_to_pip(monkeypatch):
    monkeypatch.setattr(sh.shutil, "which", lambda name: None)
    cmd = sh._install_cmd(".[convert]", "/venv/bin/python")
    assert cmd == ["/venv/bin/python", "-m", "pip", "install", ".[convert]"]


def test_bootstrap_reports_failure_when_post_install_import_fails(monkeypatch, tmp_path):
    """A zero-exit install with a broken import must report failure, not success."""
    # Pretend the venv already exists so we skip the create step.
    monkeypatch.setattr(sh, "_VENV_DIR", tmp_path / ".venv")
    (tmp_path / ".venv").mkdir()
    monkeypatch.setattr(sh.shutil, "which", lambda name: None)

    calls = []

    def fake_run(cmd, **kwargs):
        calls.append(cmd)
        # The install command succeeds...
        if "install" in cmd:
            return _fake_completed(0)
        # ...but the `-c "import markitdown"` probe fails.
        if "-c" in cmd:
            return _fake_completed(1, stderr="ModuleNotFoundError: No module named 'markitdown'")
        return _fake_completed(0)

    monkeypatch.setattr(sh.subprocess, "run", fake_run)
    result = sh.bootstrap_environment(extra="convert")
    assert result["installed"] is False
    assert result["error"] and "importable" in result["error"]
    # The import probe was actually attempted.
    assert any("-c" in c for c in calls)


def test_bootstrap_reports_failure_when_import_probe_times_out(monkeypatch, tmp_path):
    """A wedged import probe times out -> installed False, clear error, and the
    probe uses the short probe budget, not the 10-minute install timeout."""
    monkeypatch.setattr(sh, "_VENV_DIR", tmp_path / ".venv")
    (tmp_path / ".venv").mkdir()
    monkeypatch.setattr(sh.shutil, "which", lambda name: None)

    probe_timeouts = []

    def fake_run(cmd, **kwargs):
        # The install command succeeds...
        if "install" in cmd:
            return _fake_completed(0)
        # ...but the `-c "import markitdown"` probe hangs and gets killed.
        if "-c" in cmd:
            probe_timeouts.append(kwargs.get("timeout"))
            raise sh.subprocess.TimeoutExpired(cmd=cmd, timeout=kwargs.get("timeout"))
        return _fake_completed(0)

    monkeypatch.setattr(sh.subprocess, "run", fake_run)
    result = sh.bootstrap_environment(extra="convert")

    assert result["installed"] is False
    assert result["error"] and "importable" in result["error"]
    # The probe ran with the short budget, never the 10-minute install timeout.
    assert probe_timeouts == [sh._IMPORT_PROBE_TIMEOUT]
    assert sh._IMPORT_PROBE_TIMEOUT < sh._INSTALL_TIMEOUT
    assert sh._INSTALL_TIMEOUT not in probe_timeouts


def test_bootstrap_succeeds_when_import_verifies(monkeypatch, tmp_path):
    monkeypatch.setattr(sh, "_VENV_DIR", tmp_path / ".venv")
    (tmp_path / ".venv").mkdir()
    monkeypatch.setattr(sh.shutil, "which", lambda name: None)
    monkeypatch.setattr(sh.subprocess, "run", lambda cmd, **kw: _fake_completed(0))
    result = sh.bootstrap_environment(extra="convert")
    assert result["installed"] is True
    assert result["error"] is None


def test_doctor_reports_without_installing(monkeypatch):
    called = []
    monkeypatch.setattr(sh, "_pip_install", lambda spec: called.append(spec) or True)
    report = sh.doctor()
    assert "python_packages" in report and "system_tools" in report
    assert "pandoc" in report["system_tools"]
    assert called == []  # doctor never installs
