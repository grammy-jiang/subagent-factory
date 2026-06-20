"""Tests for the deterministic structure-aware Markdown chunker (per-book MAP-inner)."""

from tools.subagent_factory.chunk_source import chunk_markdown


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
