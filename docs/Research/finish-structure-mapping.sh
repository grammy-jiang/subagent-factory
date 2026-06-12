#!/usr/bin/env bash
#
# finish-structure-mapping.sh — finish the long-document-structure-mapping research.
#
# Plain and simple: it builds a prompt (below), calls the `claude` CLI with it, and
# runs in the FOREGROUND — no setsid, no &, no detach, no PID files. It blocks your
# terminal until the research finishes (tens of minutes), streaming progress.
#
# RUN IT (in your own terminal):
#     bash docs/Research/finish-structure-mapping.sh
#
#   - Ctrl-C stops it. Re-run to resume (the research-pipeline picks up where it left off).
#   - Closing the terminal stops it (it's foreground). If you want it to survive that,
#     run:   nohup bash docs/Research/finish-structure-mapping.sh > finish.out 2>&1 &
#
set -uo pipefail

REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
TOPIC_DIR="$REPO/docs/Research/long-document-structure-mapping"
CLAUDE_BIN="${CLAUDE_BIN:-claude}"   # the claude CLI on your PATH (override with CLAUDE_BIN=...)
MODEL="${MODEL:-opus}"

# ─────────────────────────────────────────────────────────────────────────────
# THE PROMPT — edit freely. This is the entire instruction sent to claude.
# ─────────────────────────────────────────────────────────────────────────────
PROMPT="$(cat <<'EOF'
Finish the in-progress research run in your CURRENT WORKING DIRECTORY using the
research-pipeline skill (deep profile). A round-1 report and pipeline state already exist
here (workflow_state.json, round_state.json, and a *-research-report.md). Your job is to
CLOSE the two open HIGH academic gaps and finalise.

TOPIC: Hierarchical reading of long technical/scientific documents for distillation —
long-document/hierarchical summarisation, topic/discourse segmentation, document-structure
extraction, and candidate knowledge-unit identification over 200+ page books.

OPEN HIGH GAPS TO CLOSE (run gap-closure rounds per the research-pipeline iterative-synthesis
rules: new run_id, carry prior paper ids):
- G1 — standalone topic / linear text segmentation (TextTiling, C99, BayesSeg, neural text
  segmentation). Segment boundaries gate candidate-unit recall.
  Queries: "neural text segmentation topic boundary detection long document supervised";
           "TextTiling C99 BayesSeg linear text segmentation coherence".
- G3 — claim / principle-level RECALL evaluation (current report has only summarisation-QA and
  keyphrase proxies).
  Queries: "claim extraction recall evaluation long document benchmark check-worthy";
           "key point analysis coverage evaluation argument mining".

HOW:
- Use the research-pipeline skill exactly as in the prior rounds. Resume from the existing
  workflow_state.json in this folder; if it cannot resume, start fresh gap-closure rounds that
  carry the prior paper ids. When the pipeline prints DELEGATE TO SUB-AGENT, run the named
  sub-agent (paper-screener / paper-analyzer / paper-synthesizer) with the printed contract and
  continue. Honor reviewer gates (on 'rejected': fix, reset task, re-run).
- Run gap-closure rounds until BOTH HIGH gaps are closed or reclassified, or the 4-round cap is
  reached.
- Update the final report *-research-report.md with the new findings — in particular a concrete
  topic-segmentation method recommendation for pipeline stage 2, and a claim/principle-recall
  evaluation method to use as the Step-10 source-map coverage gate.

SANDBOX (hard): work ONLY in this folder and the shared ~/.cache pipeline cache. Do NOT modify
the subagent-factory repository.

WHEN DONE — ALWAYS, as your final action — write SUMMARY.md in this folder with:
  1. final report filename;
  2. the Round History table;
  3. every remaining open gap (classification ACADEMIC/ENGINEERING, severity, one line on why);
  4. the 5–10 findings most relevant to building a Tier-1 source-structure-mapping preprocessor,
     each with paper IDs.
Then print exactly: RESEARCH RUN COMPLETE: <report filename>
EOF
)"
# ─────────────────────────────────────────────────────────────────────────────

[ -d "$TOPIC_DIR" ] || { echo "topic folder missing: $TOPIC_DIR" >&2; exit 1; }
command -v "$CLAUDE_BIN" >/dev/null 2>&1 || { echo "claude CLI not found on PATH (set CLAUDE_BIN=)" >&2; exit 1; }

# Safety: don't start a second run on the same folder (they would clobber each other).
if pgrep -fa "claude -p" 2>/dev/null | grep -qi "structure-mapping\|long technical/scientific"; then
  echo "A research 'claude -p' process already seems to be running on this topic."
  echo "Two runs share one folder and will clobber each other. Check:"
  echo "    ps aux | grep 'claude -p'"
  echo "Kill the stray one, then re-run this script. Aborting."
  exit 1
fi

cd "$TOPIC_DIR"   # the research-pipeline sandboxes to the current directory
echo "Finishing research in: $TOPIC_DIR"
echo "Foreground run — blocks until done. Ctrl-C to stop, re-run to resume."
echo

"$CLAUDE_BIN" -p "$PROMPT" \
    --model "$MODEL" \
    --dangerously-skip-permissions \
    --verbose 2>&1 | tee -a run.log

echo
echo "Finished. Check:"
echo "  $TOPIC_DIR/SUMMARY.md"
echo "  $TOPIC_DIR/long-document-structure-mapping-research-report.md"
