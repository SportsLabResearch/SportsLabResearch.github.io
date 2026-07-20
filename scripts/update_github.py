from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
import requests

from config import GITHUB_API, GITHUB_ORG, GITHUB_OUTPUT, REQUEST_TIMEOUT

HEADERS = {
    "Accept": "application/vnd.github+json",
    "User-Agent": "SportsLabResearch-Website-Updater/1.0",
}

def get_repositories() -> list[dict]:
    r = requests.get(
        f"{GITHUB_API}/orgs/{GITHUB_ORG}/repos",
        params={"type": "public", "sort": "updated", "direction": "desc", "per_page": 100},
        headers=HEADERS,
        timeout=REQUEST_TIMEOUT,
    )
    r.raise_for_status()
    return r.json()

def get_latest_release(repository: str) -> dict | None:
    r = requests.get(
        f"{GITHUB_API}/repos/{GITHUB_ORG}/{repository}/releases/latest",
        headers=HEADERS,
        timeout=REQUEST_TIMEOUT,
    )
    if r.status_code == 404:
        return None
    r.raise_for_status()
    return r.json()

def fmt_date(value: str | None) -> str:
    if not value:
        return "—"
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00")).strftime("%d/%m/%Y")
    except ValueError:
        return value

def build_markdown(repositories: list[dict]) -> str:
    updated = datetime.now(timezone.utc).strftime("%d/%m/%Y %H:%M UTC")
    lines = [
        "---", "hide:", "  - toc", "---", "",
        "# Software", "",
        "Software repositories synchronized automatically from GitHub.", "",
        f"**Last automatic update:** {updated}", "", "---", ""
    ]

    for repo in repositories:
        name = repo["name"]
        description = repo.get("description") or "Scientific software developed by SportsLabResearch."
        release = get_latest_release(name)

        lines += [
            f"## {name}", "",
            description, "",
            f"- **Repository:** [{repo['html_url']}]({repo['html_url']})",
            f"- **Last GitHub update:** {fmt_date(repo.get('updated_at'))}",
            f"- **Primary language:** {repo.get('language') or '—'}",
        ]

        if release:
            tag = release.get("tag_name") or release.get("name") or "Latest release"
            url = release.get("html_url") or repo["html_url"]
            lines += [
                f"- **Latest release:** [{tag}]({url})",
                f"- **Release date:** {fmt_date(release.get('published_at'))}",
            ]
        else:
            lines.append("- **Latest release:** No published release")

        if repo.get("homepage"):
            homepage = repo["homepage"]
            lines.append(f"- **Documentation / website:** [{homepage}]({homepage})")

        lines += ["", "---", ""]

    lines += ["> This page is generated automatically from the GitHub REST API.", ""]
    return "\n".join(lines)

def main() -> int:
    repos = [r for r in get_repositories() if not r.get("fork") and not r.get("archived")]
    out = Path(GITHUB_OUTPUT)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(build_markdown(repos), encoding="utf-8")
    print(f"GitHub actualizado: {len(repos)} repositorios")
    print(f"Archivo generado: {out}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
