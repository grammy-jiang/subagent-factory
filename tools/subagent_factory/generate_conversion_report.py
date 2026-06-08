"""Generate conversion report Markdown from conversion result."""

from datetime import datetime, timezone
from pathlib import Path

from jinja2 import Environment, FileSystemLoader


_TEMPLATES_DIR = Path(__file__).parent.parent.parent / "templates"


def generate_conversion_report(
    source_id: str,
    original_filename: str,
    conversion_result: dict,
    output_path: str | Path,
) -> dict:
    """
    Generate Markdown conversion report and write to output_path.

    Also generates human-review queue entry if review is required.
    Returns report data dict.
    """
    stats = conversion_result.get("stats", {})
    warnings = conversion_result.get("warnings", [])
    errors = conversion_result.get("errors", [])

    is_scanned = conversion_result.get("is_scanned", False)
    human_review_required = bool(errors) or is_scanned
    human_review_reasons = []
    if is_scanned:
        human_review_reasons.append("Possible scanned/image-only PDF — OCR may be required")
    if errors:
        human_review_reasons.extend(errors)

    report = {
        "schema_version": "conversion-report-v1",
        "source_id": source_id,
        "original_filename": original_filename,
        "conversion_status": conversion_result.get("conversion_status", "ok"),
        "converter_used": conversion_result.get("converter_used"),
        "warnings": warnings,
        "errors": errors,
        "human_review_required": human_review_required,
        "human_review_reasons": human_review_reasons,
        "stats": stats,
        "generated_at": datetime.now(timezone.utc).isoformat(),
    }

    env = Environment(loader=FileSystemLoader(str(_TEMPLATES_DIR)), autoescape=False)
    tmpl = env.get_template("conversion-report.md.j2")
    rendered = tmpl.render(**report)
    Path(output_path).write_text(rendered, encoding="utf-8")

    return report
