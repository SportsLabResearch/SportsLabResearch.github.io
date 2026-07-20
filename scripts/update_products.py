from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path

from config import GITHUB_DATA, PRODUCTS_OUTPUT, ZENODO_DATA


def normalize(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", value.casefold())


def clean_text(value: str) -> str:
    return " ".join((value or "").split())


def format_date(value: str) -> str:
    if not value:
        return "—"
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00")).strftime("%d/%m/%Y")
    except ValueError:
        return value


def load_json(path: str) -> dict:
    file_path = Path(path)
    if not file_path.exists():
        return {}
    try:
        return json.loads(file_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}


def find_zenodo_record(repository_name: str, records: list[dict]) -> dict | None:
    candidates = {
        normalize(repository_name),
        normalize(repository_name.replace("SportsLabResearch-", "")),
    }
    for record in records:
        title = normalize(record.get("title", ""))
        if any(candidate and candidate in title for candidate in candidates):
            return record
    return None


def button(label: str, url: str) -> str:
    if url:
        return f'[{label}]({url}){{ .md-button target="_blank" rel="noopener" }}'
    return f'<span class="md-button slr-button-disabled" aria-disabled="true">{label}</span>'


def build_card(repo: dict, records: list[dict]) -> list[str]:
    name = repo.get("name") or "Product"
    release = repo.get("release") or {}
    record = find_zenodo_record(name, records)
    doi = (record or {}).get("doi") or "Not available"
    zenodo_url = (record or {}).get("record_url") or ""

    return [
        f"-   ## {name}",
        "",
        f"    {clean_text(repo.get('description') or 'Scientific software developed by SportsLabResearch.')}",
        "",
        '    <div class="slr-product-actions" markdown>',
        f"    {button('GitHub', repo.get('repository_url') or '')}",
        f"    {button('Documentation', repo.get('documentation_url') or '')}",
        f"    {button('Zenodo', zenodo_url)}",
        "    </div>",
        "",
        '    <div class="slr-product-meta" markdown>',
        f"    **Latest release:** {release.get('tag') or 'No published release'}  ",
        f"    **Release date:** {format_date(release.get('published_at', ''))}  ",
        f"    **DOI:** {doi}  ",
        f"    **Language:** {repo.get('language') or '—'}  ",
        f"    **License:** {repo.get('license') or '—'}",
        "    </div>",
        "",
    ]


def build_markdown(github: dict, zenodo: dict) -> str:
    repositories = github.get("repositories", [])
    records = zenodo.get("records", [])
    updated = datetime.now().strftime("%d/%m/%Y %H:%M")

    lines = [
        "---",
        "hide:",
        "  - toc",
        "---",
        "",
        "# Products",
        "",
        "Each product is presented as a single unified record combining GitHub, documentation, releases and Zenodo.",
        "",
        f"**Last automatic update:** {updated}",
        "",
        '<div class="grid cards slr-products" markdown>',
        "",
    ]
    for repo in repositories:
        lines.extend(build_card(repo, records))
    lines.extend(["</div>", "", "> Automatically generated from GitHub and Zenodo.", ""])
    return "\n".join(lines)


def main() -> int:
    output = Path(PRODUCTS_OUTPUT)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        build_markdown(load_json(GITHUB_DATA), load_json(ZENODO_DATA)),
        encoding="utf-8",
    )
    print(f"Productos unificados: {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
