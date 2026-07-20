from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

import requests

from config import REQUEST_TIMEOUT, ZENODO_API, ZENODO_DATA, ZENODO_QUERY

HEADERS = {
    "Accept": "application/json",
    "User-Agent": "SportsLabResearch-Website-Updater/3.0",
}


def get_records() -> list[dict]:
    response = requests.get(
        ZENODO_API,
        params={"q": ZENODO_QUERY, "sort": "mostrecent", "size": 25},
        headers=HEADERS,
        timeout=REQUEST_TIMEOUT,
    )
    response.raise_for_status()
    return response.json().get("hits", {}).get("hits", [])


def main() -> int:
    records: list[dict] = []

    for record in get_records():
        metadata = record.get("metadata") or {}
        links = record.get("links") or {}
        record_id = record.get("id")
        records.append(
            {
                "id": record_id,
                "title": metadata.get("title") or "",
                "description": metadata.get("description") or "",
                "doi": metadata.get("doi") or record.get("doi") or "",
                "version": metadata.get("version") or "",
                "publication_date": metadata.get("publication_date") or "",
                "record_url": links.get("html")
                or f"https://zenodo.org/records/{record_id}",
                "creators": [
                    creator.get("name", "")
                    for creator in metadata.get("creators", [])
                    if creator.get("name")
                ],
            }
        )

    output = Path(ZENODO_DATA)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(
            {
                "source": "https://zenodo.org/",
                "updated_at": datetime.now(timezone.utc).isoformat(),
                "records": records,
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )
    print(f"Zenodo actualizado: {len(records)} registros")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
