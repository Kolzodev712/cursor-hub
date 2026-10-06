"""Merge wizard-managed doctrine markdown without deleting project-owned prose."""
from __future__ import annotations

LEGACY_RECONCILE_MARKER = "<!-- doctrine-setup:legacy-preserved -->"


def merge_managed_markdown(
    existing: str | None,
    new_managed: str,
    *,
    section_header: str,
    marker: str,
) -> str:
    """
    Replace the setup-owned region (section_header through marker inclusive).
    Preserve preamble before section_header and epilogue after marker.
    Legacy files without the expected header are kept intact with a reconciliation notice.
    """
    if not existing or not existing.strip():
        return new_managed
    text = existing
    if section_header not in text:
        notice = (
            f"\n\n{LEGACY_RECONCILE_MARKER}\n"
            "> Legacy doctrine content preserved above. "
            "Review for conflicts with the managed section below before approving.\n"
        )
        return text.rstrip() + notice + "\n" + new_managed
    preamble = text.split(section_header, 1)[0]
    if marker in text:
        epilogue = text.split(marker, 1)[1]
    else:
        epilogue = ""
    return preamble + new_managed + epilogue
