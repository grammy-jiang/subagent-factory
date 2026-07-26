"""The CLI slug guard (cli_support.subagent_path): every `cli <verb> <slug>` command derives its
package path through this, so its kebab-case gate is the single control stopping a slug from escaping
subagents/ (absolute path, .. traversal, or an embedded /). Untested until now."""

import click
import pytest

from tools.subagent_factory.cli_support import repo_root, subagent_path


@pytest.mark.parametrize(
    "bad",
    [
        "../../etc",  # parent traversal
        "/abs",  # absolute path
        "Has_Upper",  # underscore + uppercase (not kebab-case)
        "-leading",  # leading hyphen (must start [a-z0-9])
        "has/slash",  # embedded separator
        "..",  # bare traversal
        "",  # empty
        "a b",  # whitespace
    ],
)
def test_subagent_path_rejects_unsafe_slug(bad):
    with pytest.raises(click.BadParameter):
        subagent_path(bad)


def test_subagent_path_valid_slug_stays_under_subagents():
    p = subagent_path("python-reviewer")
    assert p == repo_root() / "subagents" / "python-reviewer"
    # the resolved path must not escape the subagents/ root
    assert (repo_root() / "subagents") in p.parents
