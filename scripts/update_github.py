from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

import requests

from config import (
    DISPLAY_REPOSITORIES,
    GITHUB_API,
    GITHUB_DATA,
    GITHUB_ORG,
    REQUEST_TIMEOUT,
)

HEADERS = {
    "Accept": "application/vnd.github+json",
    "User-Agent": "SportsLabResearch-Website-Updater/3.0",
}


def request_json(url: str) -> dict | list | None:
    response = requests.get(url, headers=HEADERS, timeout=REQUEST_TIMEOUT)
    if response.status_code == 404:
        return None
    response.raise_for_status()
    return response.json()


def url_exists(url: str) -> bool:
    try:
        response = requests.get(
            url,
            headers={"User-Agent": HEADERS["User-Agent"]},
            timeout=REQUEST_TIMEOUT,
            allow_redirects=True,
            stream=True,
        )
        return response.status_code < 400
    except requests.RequestException:
        return False


def get_repository(name: str) -> dict | None:
    data = request_json(f"{GITHUB_API}/repos/{GITHUB_ORG}/{name}")
    return data if isinstance(data, dict) else None


def get_latest_release(name: str) -> dict | None:
    data = request_json(f"{GITHUB_API}/repos/{GITHUB_ORG}/{name}/releases/latest")
    return data if isinstance(data, dict) else None


def documentation_url(repo: dict) -> str:
    homepage = (repo.get("homepage") or "").strip()
    expected = f"https://sportslabresearch.github.io/{repo['name']}/"

    if homepage and url_exists(homepage):
        return homepage
    if url_exists(expected):
        return expected
    return ""


def main() -> int:
    repositories: list[dict] = []

    for name in DISPLAY_REPOSITORIES:
        repo = get_repository(name)
        if not repo or repo.get("archived") or repo.get("fork"):
            continue

        release = get_latest_release(name) or {}
        repositories.append(
            {
                "name": name,
                "description": repo.get("description")
                or "Scientific software developed by SportsLabResearch.",
                "repository_url": repo.get("html_url") or "",
                "documentation_url": documentation_url(repo),
                "language": repo.get("language") or "",
                "license": (repo.get("license") or {}).get("spdx_id") or "—",
                "updated_at": repo.get("updated_at") or "",
                "topics": repo.get("topics") or [],
                "release": {
                    "tag": release.get("tag_name") or "",
                    "name": release.get("name") or "",
                    "url": release.get("html_url") or "",
                    "published_at": release.get("published_at") or "",
                },
            }
        )

    payload = {
        "source": f"https://github.com/{GITHUB_ORG}",
        "updated_at": datetime.now(timezone.utc).isoformat(),
        "repositories": repositories,
    }

    output = Path(GITHUB_DATA)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"GitHub actualizado: {len(repositories)} repositorios seleccionados")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
