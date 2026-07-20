from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
import requests

from config import REQUEST_TIMEOUT, ZENODO_API, ZENODO_OUTPUT, ZENODO_QUERY

HEADERS = {
    "Accept": "application/json",
    "User-Agent": "SportsLabResearch-Website-Updater/1.0",
}

def get_records() -> list[dict]:
    r = requests.get(
        ZENODO_API,
        params={
            "q": ZENODO_QUERY,
            "sort": "mostrecent",
            "size": 25,
            "all_versions": "false",
        },
        headers=HEADERS,
        timeout=REQUEST_TIMEOUT,
    )
    r.raise_for_status()
    return r.json().get("hits", {}).get("hits", [])

def fmt_date(value: str | None) -> str:
    if not value:
        return "—"
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00")).strftime("%d/%m/%Y")
    except ValueError:
        return value

def creators(metadata: dict) -> str:
    names = [c.get("name", "").strip() for c in metadata.get("creators", [])]
    return ", ".join(n for n in names if n) or "—"

def build_markdown(records: list[dict]) -> str:
    updated = datetime.now(timezone.utc).strftime("%d/%m/%Y %H:%M UTC")
    lines = [
        "---", "hide:", "  - toc", "---", "",
        "# Zenodo", "",
        "Records synchronized automatically from Zenodo.", "",
        f"**Last automatic update:** {updated}", "", "---", ""
    ]

    if not records:
        lines += ["_No SportsLabResearch records were found with the configured query._", ""]

    for record in records:
        md = record.get("metadata") or {}
        title = md.get("title") or f"Zenodo record {record.get('id', '')}"
        doi = md.get("doi") or record.get("doi") or "—"
        version = md.get("version") or "—"
        url = record.get("links", {}).get("html") or f"https://zenodo.org/records/{record.get('id')}"

        lines += [
            f"## {title}", "",
            f"- **Creators:** {creators(md)}",
            f"- **Publication date:** {fmt_date(md.get('publication_date'))}",
            f"- **Version:** {version}",
            f"- **DOI:** {doi}",
            f"- **Record:** [{url}]({url})",
            "", "---", ""
        ]

    lines += ["> This page is generated automatically from the Zenodo Records API.", ""]
    return "\n".join(lines)

def main() -> int:
    records = get_records()
    out = Path(ZENODO_OUTPUT)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(build_markdown(records), encoding="utf-8")
    print(f"Zenodo actualizado: {len(records)} registros")
    print(f"Archivo generado: {out}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
