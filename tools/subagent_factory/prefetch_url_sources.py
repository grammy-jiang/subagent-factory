"""Prefetch URL sources into the snapshot cache BEFORE a network-denied author session (item #1, leg C).

The author/ingest session reads untrusted source content while holding powerful tools; the "lethal
trifecta" is broken by removing its network leg. But URL sources still need fetching. This step does
that fetching deterministically and up front — over the network, SSRF-guarded by ``fetch_url`` — and
stores each snapshot in the URL cache (``fetch_url``'s ``cache_dir``). The subsequent author session
runs with ``SUBAGENT_FACTORY_OFFLINE=1`` so its in-session ingest serves those URLs from the warmed
cache instead of fetching, and ``--disallowedTools WebFetch WebSearch`` removes the agent's own reach
to the network. Local-file sources are passed through untouched (nothing to fetch).

CLI: ``python -m tools.subagent_factory.prefetch_url_sources <url-or-path> ...`` — exits non-zero if
any URL failed to prefetch, so the caller can abort before starting an offline session that would
then hard-fail on that URL.
"""

import shutil
import sys
import tempfile
from pathlib import Path

from tools.subagent_factory.fetch_url import DEFAULT_URL_CACHE, fetch_url


def _is_url(s: str) -> bool:
    return s.startswith("http://") or s.startswith("https://")


def prefetch_url_sources(sources: list[str], cache_dir: str | Path | None = None) -> dict:
    """Fetch every URL in ``sources`` into the cache; pass local paths through.

    Returns ``{cached: [url...], skipped: [path...], errors: [{url, error}...]}``.
    """
    cache = Path(cache_dir) if cache_dir else DEFAULT_URL_CACHE
    out: dict = {"cached": [], "skipped": [], "errors": []}
    scratch = Path(tempfile.mkdtemp(prefix="subagent-prefetch-"))
    try:
        for s in sources:
            if not _is_url(s):
                out["skipped"].append(s)
                continue
            r = fetch_url(s, scratch, cache_dir=cache, offline=False)
            if r.get("error"):
                out["errors"].append({"url": s, "error": r["error"]})
            else:
                out["cached"].append(s)
    finally:
        shutil.rmtree(scratch, ignore_errors=True)  # snapshots are throwaway; the cache is durable
    return out


def main() -> None:
    if len(sys.argv) < 2:
        print(
            "Usage: python -m tools.subagent_factory.prefetch_url_sources <url-or-path> ...",
            file=sys.stderr,
        )
        sys.exit(2)
    res = prefetch_url_sources(sys.argv[1:])
    for u in res["cached"]:
        print(f"prefetched: {u}")
    for e in res["errors"]:
        print(f"PREFETCH FAILED: {e['url']} — {e['error']}", file=sys.stderr)
    print(
        f"prefetch: {len(res['cached'])} cached, {len(res['skipped'])} local, "
        f"{len(res['errors'])} failed"
    )
    sys.exit(1 if res["errors"] else 0)


if __name__ == "__main__":
    main()
