from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

import requests

from config import GITHUB_API, GITHUB_DATA, GITHUB_ORG, REQUEST_TIMEOUT

HEADERS = {
    "Accept": "application/vnd.github+json",
    "User-Agent": "SportsLabResearch-Website-Updater/2.0",
}


def get_repositories() -> list[dict]:
    response = requests.get(
        f"{GITHUB_API}/orgs/{GITHUB_ORG}/repos",
        params={
            "type": "public",
            "sort": "updated",
            "direction": "desc",
            "per_page": 100,
        },
        headers=HEADERS,
        timeout=REQUEST_TIMEOUT,
    )
    response.raise_for_status()
    return response.json()


def get_latest_release(repository: str) -> dict | None:
    response = requests.get(
        f"{GITHUB_API}/repos/{GITHUB_ORG}/{repository}/releases/latest",
        headers=HEADERS,
        timeout=REQUEST_TIMEOUT,
    )
    if response.status_code == 404:
        return None
    response.raise_for_status()
    return response.json()


def main() -> int:
    repositories: list[dict] = []

    for repo in get_repositories():
        if repo.get("fork") or repo.get("archived"):
            continue

        release = get_latest_release(repo["name"])
        repositories.append(
            {
                "name": repo["name"],
                "description": repo.get("description") or "Scientific software developed by SportsLabResearch.",
                "repository_url": repo["html_url"],
                "homepage": repo.get("homepage") or "",
                "language": repo.get("language") or "",
                "updated_at": repo.get("updated_at") or "",
                "topics": repo.get("topics") or [],
                "release": {
                    "tag": (release or {}).get("tag_name") or "",
                    "name": (release or {}).get("name") or "",
                    "url": (release or {}).get("html_url") or "",
                    "published_at": (release or {}).get("published_at") or "",
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

    print(f"GitHub actualizado: {len(repositories)} repositorios")
    print(f"Datos guardados: {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
