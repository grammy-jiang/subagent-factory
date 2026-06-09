"""Tests for the test-results.md writer (v0 Phase 10 artifact)."""

import yaml

from tools.subagent_factory.run_tests import write_test_results


def _make_pkg(tmp_path):
    pkg = tmp_path / "subagents" / "demo"
    tests_dir = pkg / "tests"
    tests_dir.mkdir(parents=True)
    (tests_dir / "golden-tests.yaml").write_text(
        yaml.safe_dump(
            {
                "golden_tests": [{"test_id": "GT-001", "description": "positive route"}],
                "negative_routing_tests": [{"test_id": "NR-001", "description": "no route"}],
            }
        ),
        encoding="utf-8",
    )
    return pkg


def test_write_test_results_creates_file(tmp_path):
    pkg = _make_pkg(tmp_path)
    out = write_test_results(pkg)
    assert out.exists()
    assert out.name == "test-results.md"
    body = out.read_text(encoding="utf-8")
    assert "Test Results" in body
    assert "GT-001" in body
    assert "NR-001" in body


def test_write_test_results_includes_self_check_verdict(tmp_path):
    pkg = _make_pkg(tmp_path)
    self_check = {
        "verdict": "PASS",
        "findings": [{"num": 1, "level": "PASS", "check": "slug", "message": "ok"}],
    }
    out = write_test_results(pkg, self_check_result=self_check)
    body = out.read_text(encoding="utf-8")
    assert "Phase 8 Profile Self-Check" in body
    assert "PASS" in body
    assert "slug" in body
