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
    repo_key = normalize(repository_name)
    repo_without_prefix = normalize(
        repository_name.replace("SportsLabResearch-", "")
    )

    for record in records:
        title_key = normalize(record.get("title", ""))

        if repo_key and repo_key in title_key:
            return record

        if repo_without_prefix and repo_without_prefix in title_key:
            return record

    return None


def active_button(label: str, url: str, icon: str) -> str:
    return (
        f'[{label}]({url})'
        '{ .md-button target="_blank" rel="noopener" }'
    )


def inactive_button(label: str, icon: str) -> str:
    return (
        f'<span class="md-button" '
        f'style="opacity:0.40; cursor:not-allowed; pointer-events:none;" '
        f'aria-disabled="true">{label}</span>'
    )


def build_product_card(repo: dict, records: list[dict]) -> list[str]:
    name = repo.get("name") or "Product"
    description = clean_text(
        repo.get("description")
        or "Scientific software developed by SportsLabResearch."
    )

    repository_url = repo.get("repository_url") or ""
    documentation_url = repo.get("homepage") or f"https://sportslabresearch.github.io/{name}/"
    release = repo.get("release") or {}
    record = find_zenodo_record(name, records)

    zenodo_url = ""
    doi = "Not available"
    zenodo_version = "—"

    if record:
        zenodo_url = record.get("record_url") or ""
        doi = record.get("doi") or "Not available"
        zenodo_version = record.get("version") or "—"

    github_button = (
        active_button("GitHub", repository_url, ":material-github:")
        if repository_url
        else inactive_button("GitHub", "◉")
    )

    documentation_button = (
        active_button(
            "Documentation",
            documentation_url,
            ":material-book-open-page-variant:",
        )
        if documentation_url
        else inactive_button("Documentation", "▤")
    )

    zenodo_button = (
        active_button("Zenodo", zenodo_url, ":material-database:")
        if zenodo_url
        else inactive_button("Zenodo", "◆")
    )

    release_tag = release.get("tag") or "No published release"
    release_date = format_date(release.get("published_at", ""))
    language = repo.get("language") or "—"

    return [
        f"-   ## {name}",
        "",
        f"    {description}",
        "",
        "    <div style=\"display:grid;grid-template-columns:repeat(3,1fr);gap:8px;\" markdown>",
        f"    {github_button}",
        f"    {documentation_button}",
        f"    {zenodo_button}",
        "    </div>",
        "",
        "    <div markdown>",
        "",
        f"    **Latest release:** {release_tag}  ",
        f"    **Release date:** {release_date}  ",
        f"    **DOI:** {doi}  ",
        f"    **Zenodo version:** {zenodo_version}  ",
        f"    **Primary language:** {language}",
        "",
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
        (
            "Scientific products developed by SportsLabResearch. "
            "Each card provides direct access to GitHub, documentation "
            "and Zenodo."
        ),
        "",
        f"**Last automatic update:** {updated}",
        "",
    ]

    if not repositories:
        lines.extend(
            [
                "!!! warning",
                "    No products are currently available.",
                "",
            ]
        )
    else:
        lines.extend(
            [
                '<div class="grid cards" markdown>',
                "",
            ]
        )

        for repo in repositories:
            lines.extend(build_product_card(repo, records))

        lines.extend(
            [
                "</div>",
                "",
            ]
        )

    lines.extend(
        [
            "---",
            "",
            "> This page is generated automatically from GitHub and Zenodo.",
            "",
        ]
    )

    return "\n".join(lines)


def main() -> int:
    github = load_json(GITHUB_DATA)
    zenodo = load_json(ZENODO_DATA)

    output = Path(PRODUCTS_OUTPUT)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        build_markdown(github, zenodo),
        encoding="utf-8",
    )

    print(f"Productos unificados: {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
