from __future__ import annotations

import re
import sys
from datetime import datetime
from pathlib import Path
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup, Tag


SOURCE_URL = (
    "https://webs.um.es/josepinoortega/miwiki/"
    "doku.php?id=investigacion"
)

PROJECT_ROOT = Path(__file__).resolve().parent.parent
OUTPUT_FILE = PROJECT_ROOT / "docs" / "publications.md"

GENERAL_SECTIONS = {
    "books": "Books",
    "chapter books": "Book Chapters",
    "doctoral thesis": "Doctoral Theses",
    "conferences": "Conferences",
}

PUBLICATION_YEARS = {"2026", "2025", "2024"}


def clean_text(text: str) -> str:
    text = text.replace("\xa0", " ")
    text = re.sub(r"\s+", " ", text).strip()
    text = text.replace(" .", ".")
    text = text.replace(" ,", ",")
    return text


def is_separator(text: str) -> bool:
    value = text.strip()

    if not value:
        return True

    return bool(re.fullmatch(r"[-–—_•·\s]+", value))


def normalize_heading(text: str) -> str:
    text = clean_text(text)
    text = text.rstrip(":")
    return text.casefold()


def detect_section(text: str) -> tuple[str | None, bool]:
    """
    Devuelve:
      - nombre interno de la sección;
      - True cuando el texto representa un encabezado.
    """
    normalized = normalize_heading(text)

    year_match = re.fullmatch(
        r"recent research papers\s*[—–-]?\s*\(?(\d{4})\)?",
        normalized,
    )

    if year_match:
        year = year_match.group(1)

        if year in PUBLICATION_YEARS:
            return f"Research Papers — {year}", True

        # Al llegar a 2023 o a cualquier otro año,
        # se cierra la extracción de los años seleccionados.
        return None, True

    if normalized in GENERAL_SECTIONS:
        return GENERAL_SECTIONS[normalized], True

    return None, False


def element_to_markdown(element: Tag) -> str:
    parts: list[str] = []

    for child in element.children:
        if isinstance(child, Tag):
            if child.name == "a":
                label = clean_text(child.get_text(" ", strip=True))
                href = clean_text(child.get("href", ""))

                if href:
                    absolute_url = urljoin(SOURCE_URL, href)
                    parts.append(f"[{label or absolute_url}]({absolute_url})")
                elif label:
                    parts.append(label)
            else:
                value = clean_text(child.get_text(" ", strip=True))
                if value:
                    parts.append(value)
        else:
            value = clean_text(str(child))
            if value:
                parts.append(value)

    return clean_text(" ".join(parts))


def find_content_container(soup: BeautifulSoup) -> Tag:
    selectors = [
        "#dokuwiki__content",
        "div.page",
        "main",
        "article",
        "div.dokuwiki",
    ]

    for selector in selectors:
        container = soup.select_one(selector)
        if isinstance(container, Tag):
            return container

    if isinstance(soup.body, Tag):
        return soup.body

    raise RuntimeError("No se ha localizado el contenido principal.")


def extract_sections(soup: BeautifulSoup) -> dict[str, list[str]]:
    section_names = [
        "Research Papers — 2026",
        "Research Papers — 2025",
        "Research Papers — 2024",
        "Books",
        "Book Chapters",
        "Doctoral Theses",
        "Conferences",
    ]

    sections: dict[str, list[str]] = {
        section_name: [] for section_name in section_names
    }

    container = find_content_container(soup)
    current_section: str | None = None

    elements = container.find_all(
        ["h1", "h2", "h3", "h4", "h5", "p", "li"],
        recursive=True,
    )

    for element in elements:
        raw_text = clean_text(element.get_text(" ", strip=True))

        if not raw_text:
            continue

        detected_section, is_heading = detect_section(raw_text)

        if is_heading:
            current_section = detected_section
            continue

        if element.name in {"h1", "h2", "h3", "h4", "h5"}:
            current_section = None
            continue

        if current_section is None:
            continue

        item = element_to_markdown(element)

        if not item or is_separator(item):
            continue

        # Evita que títulos de años posteriores entren como publicaciones.
        _, item_is_heading = detect_section(item)
        if item_is_heading:
            current_section = None
            continue

        if item not in sections[current_section]:
            sections[current_section].append(item)

    return sections


def render_section(title: str, items: list[str]) -> str:
    lines = [f"## {title}", ""]

    if not items:
        lines.extend(
            [
                "_No records were found in this section._",
                "",
            ]
        )
        return "\n".join(lines)

    for item in items:
        lines.append(f"- {item}")

    lines.append("")
    return "\n".join(lines)


def build_markdown(sections: dict[str, list[str]]) -> str:
    updated = datetime.now().strftime("%d/%m/%Y %H:%M")

    lines = [
        "---",
        "hide:",
        "  - toc",
        "---",
        "",
        "# Publications",
        "",
        (
            "Scientific output automatically synchronized from the "
            f"[University of Murcia research profile]({SOURCE_URL})."
        ),
        "",
        f"**Last automatic update:** {updated}",
        "",
        "---",
        "",
    ]

    order = [
        "Research Papers — 2026",
        "Research Papers — 2025",
        "Research Papers — 2024",
        "Books",
        "Book Chapters",
        "Doctoral Theses",
        "Conferences",
    ]

    for title in order:
        lines.append(render_section(title, sections.get(title, [])))

    lines.extend(
        [
            "---",
            "",
            "## Scientific Profiles",
            "",
            "- [University of Murcia profile]"
            "(https://webs.um.es/josepinoortega/miwiki/doku.php?id=)",
            f"- [Research source]({SOURCE_URL})",
            "",
            "> This page is generated automatically. Manual changes may be "
            "overwritten during the next update.",
            "",
        ]
    )

    return "\n".join(lines)


def download_source() -> BeautifulSoup:
    response = requests.get(
        SOURCE_URL,
        timeout=30,
        headers={
            "User-Agent": (
                "SportsLabResearch-Publications-Updater/1.1 "
                "(https://sportslabresearch.github.io/)"
            )
        },
    )
    response.raise_for_status()

    # La página de la UMU está codificada en UTF-8.
    html = response.content.decode("utf-8", errors="replace")

    return BeautifulSoup(html, "html.parser")


def main() -> int:
    try:
        soup = download_source()
        sections = extract_sections(soup)

        total_items = sum(len(items) for items in sections.values())

        if total_items == 0:
            raise RuntimeError(
                "No se han encontrado registros en la página de la UMU."
            )

        OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
        OUTPUT_FILE.write_text(
            build_markdown(sections),
            encoding="utf-8",
        )

        print("Actualización completada.")
        print(f"Fuente: {SOURCE_URL}")
        print(f"Registros encontrados: {total_items}")
        print(f"Archivo generado: {OUTPUT_FILE}")

        for section_name, items in sections.items():
            print(f"  - {section_name}: {len(items)}")

        return 0

    except requests.RequestException as exc:
        print(f"Error de conexión: {exc}", file=sys.stderr)
        return 1

    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
