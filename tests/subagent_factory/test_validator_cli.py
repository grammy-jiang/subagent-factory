"""Tests for the shared leaf-validator CLI harness (validator_main)."""

import sys

import pytest

from tools.subagent_factory._validator_cli import validator_main

_USAGE = "Usage: python -m tools.subagent_factory.validate_x <arg>"


def test_no_arg_prints_usage_and_exits_1(monkeypatch, capsys):
    monkeypatch.setattr(sys, "argv", ["prog"])
    with pytest.raises(SystemExit) as exc:
        validator_main(lambda _p: ["unreached"], _USAGE)
    assert exc.value.code == 1
    out = capsys.readouterr().out
    assert out == _USAGE + "\n"


def test_clean_exits_0_no_output(monkeypatch, capsys):
    monkeypatch.setattr(sys, "argv", ["prog", "some/path"])
    seen = []
    with pytest.raises(SystemExit) as exc:
        validator_main(lambda p: seen.append(p) or [], _USAGE)
    assert exc.value.code == 0
    assert seen == ["some/path"]  # arg forwarded to the validate fn
    assert capsys.readouterr().out == ""


def test_errors_printed_and_exits_1(monkeypatch, capsys):
    monkeypatch.setattr(sys, "argv", ["prog", "some/path"])
    with pytest.raises(SystemExit) as exc:
        validator_main(lambda _p: ["first bad", "second bad"], _USAGE)
    assert exc.value.code == 1
    assert capsys.readouterr().out == "ERROR: first bad\nERROR: second bad\n"
