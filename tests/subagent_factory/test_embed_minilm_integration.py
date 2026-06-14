"""Integration test for the C1 reference embedder (embed_minilm).

Skipped unless torch/transformers are installed AND the all-MiniLM-L6-v2 snapshot is locally cached,
so it never triggers a model download on CI (the runners install torch via the `convert` extra but do
not cache the model). When present, it guards the load-bearing C1 property: the embedder discriminates
a paraphrase from an unrelated statement, which is what makes the embedding-cosine pairing useful.
"""

from pathlib import Path

import pytest

pytest.importorskip("torch")
pytest.importorskip("transformers")

_SNAP = (
    Path.home() / ".cache/huggingface/hub/models--sentence-transformers--all-MiniLM-L6-v2/snapshots"
)
if not (_SNAP.exists() and any(_SNAP.iterdir())):
    pytest.skip("all-MiniLM-L6-v2 not cached locally", allow_module_level=True)

from tools.subagent_factory.seed_principle_clusters import _cosine, embed_minilm  # noqa: E402


def test_embed_minilm_discriminates_paraphrase_from_unrelated():
    v = embed_minilm(
        [
            "authenticate the caller before authorising access",
            "verify who the user is before granting permissions",  # paraphrase of #0
            "compress payloads to reduce network bandwidth",  # unrelated
            "authenticate the caller before authorising access",  # identical to #0
        ]
    )
    assert len(v[0]) == 384
    assert _cosine(v[0], v[3]) > 0.99  # identical -> ~1.0 (model loaded real weights)
    # paraphrase clearly above unrelated -> the signal C1 relies on
    assert _cosine(v[0], v[1]) > _cosine(v[0], v[2]) + 0.2
