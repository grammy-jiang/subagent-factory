"""Tests for the deterministic structure-aware Markdown chunker (per-book MAP-inner)."""

import hashlib

from tools.subagent_factory.chunk_source import chunk_markdown, write_book_module


def test_empty_text_no_chunks():
    assert chunk_markdown("") == []


def test_single_small_doc_one_chunk():
    chunks = chunk_markdown("# Title\n\nsome body text\n", target_tokens=1000)
    assert len(chunks) == 1
    assert chunks[0].heading_path == "Title"
    assert "some body text" in chunks[0].text


def test_heading_breadcrumb_is_nested():
    md = "# Part\n\n## Chapter\n\nbody\n"
    chunks = chunk_markdown(md, target_tokens=1000)
    assert chunks[0].heading_path == "Part"
    assert "## Chapter" in chunks[0].text  # the nested heading travels inside the chunk text


def test_target_token_budget_splits_sections():
    body = "x " * 2000  # ~4000 chars (~1000 tok)
    md = "".join(f"## S{i}\n\n{body}\n\n" for i in range(5))
    chunks = chunk_markdown(md, target_tokens=1200, overlap_chars=0)
    assert len(chunks) >= 4  # 5 ~equal sections cannot pack 2-per-chunk under a 1200-tok target


def test_oversize_section_split_by_paragraphs():
    para = "p " * 1000  # ~2000 chars
    big = "\n\n".join(para for _ in range(6))  # ~12k chars, ONE heading
    chunks = chunk_markdown(f"# Big\n\n{big}\n", target_tokens=1000, overlap_chars=0)
    assert len(chunks) >= 3  # a single oversize section is paragraph-split


def test_neighbour_overlap_present_after_first_chunk():
    body = "z" * 100
    md = f"## A\n\n{body}\n\n## B\n\n{body}\n\n## C\n\n{body}\n"
    chunks = chunk_markdown(md, target_tokens=40, overlap_chars=50)
    assert len(chunks) >= 2
    assert "neighbour-overlap" in chunks[1].text  # carries the previous chunk's tail
    assert "neighbour-overlap" not in chunks[0].text  # first chunk has no predecessor


def test_sha_stable_and_content_sensitive_chunk_ids():
    md = "# T\n\nbody\n"
    assert chunk_markdown(md)[0].chunk_id == chunk_markdown(md)[0].chunk_id
    assert chunk_markdown(md)[0].chunk_id != chunk_markdown("# T\n\nother\n")[0].chunk_id


def test_preamble_before_first_heading():
    chunks = chunk_markdown("intro before any heading\n\n# Real\n\nbody\n", target_tokens=1000)
    assert chunks[0].heading_path == "(preamble)"
    assert "intro before any heading" in chunks[0].text


def test_char_offsets_are_monotonic():
    body = "w " * 2000
    md = "".join(f"## S{i}\n\n{body}\n\n" for i in range(4))
    chunks = chunk_markdown(md, target_tokens=1100, overlap_chars=0)
    starts = [c.char_start for c in chunks]
    assert starts == sorted(starts)


def test_char_offsets_slice_back_to_body():
    # char_start:char_end must reproduce the chunk's body bytes from the source (the offsets are
    # surfaced as authoritative provenance and feed emit_chunk_anchors' line numbers).
    body = "w " * 2000
    md = "".join(f"## S{i}\n\n{body}\n\n" for i in range(4))
    chunks = chunk_markdown(md, target_tokens=1100, overlap_chars=0)
    for c in chunks:
        # body == fed text minus the injected context header (overlap off)
        injected = c.text.split("-->\n\n", 1)[1]
        assert md[c.char_start : c.char_end] == injected


def test_oversize_split_pieces_reconstruct_source_exactly():
    # _split_oversize must not collapse/duplicate the "\n\n" separators (offset-exact reconstruction).
    para = "p " * 1000
    big = "\n\n".join(para for _ in range(6))
    md = f"# Big\n\n{big}\n"
    chunks = chunk_markdown(md, target_tokens=1000, overlap_chars=0)
    rebuilt = "".join(md[c.char_start : c.char_end] for c in chunks)
    assert rebuilt == md


def test_determinism_chunk_ids_invariant_to_runtime(monkeypatch):
    # Chunk ids are the map->reduce cache keys: identical input -> identical ids regardless of
    # PYTHONHASHSEED / locale / cwd. (hash randomization must not leak into the sha256-based ids.)
    md = "# T\n\n" + ("body line\n" * 50)
    ids1 = [c.chunk_id for c in chunk_markdown(md, target_tokens=500)]
    monkeypatch.setenv("PYTHONHASHSEED", "12345")
    ids2 = [c.chunk_id for c in chunk_markdown(md, target_tokens=500)]
    assert ids1 == ids2
    assert all(
        cid.split("-c")[0] == ids1[0].split("-c")[0] for cid in ids1
    )  # shared book namespace


def test_module_sha_and_chunk_sha12_agree(tmp_path):
    # write_book_module's dir <sha> and chunk-id <sha12> must derive from the same canonical bytes,
    # so sha.startswith(sha12) — even when the source has invalid UTF-8 (errors='replace').
    src = tmp_path / "book.md"
    src.write_bytes(b"# T\n\nvalid body\n\xff\xfe invalid utf8 tail\n")
    info = write_book_module(src, tmp_path / "out", target_tokens=1000)
    sha = info["sha"]
    canonical = src.read_bytes().decode("utf-8", errors="replace").encode("utf-8")
    assert sha == hashlib.sha256(canonical).hexdigest()
    chunks = chunk_markdown(src.read_bytes().decode("utf-8", errors="replace"), target_tokens=1000)
    assert sha.startswith(chunks[0].chunk_id.split("-c")[0])  # sha12 is a prefix of the dir sha
