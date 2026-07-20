from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def run_step(label: str, command: list[str], optional: bool = False) -> bool:
    print(f"\n{label}")
    print("-" * len(label))
    result = subprocess.run(command, cwd=ROOT, text=True)
    if result.returncode == 0:
        print("OK")
        return True
    if optional:
        print("AVISO: paso omitido por error.")
        return False
    raise SystemExit(result.returncode)


def main() -> int:
    print("=" * 60)
    print(" SportsLabResearch Website Updater v2.0 — Unified")
    print("=" * 60)

    publications = ROOT / "scripts" / "update_publications.py"
    if publications.exists():
        run_step(
            "[1/5] Actualizando publicaciones UMU",
            [sys.executable, str(publications)],
            optional=True,
        )
    else:
        print("\n[1/5] Publicaciones UMU")
        print("AVISO: scripts/update_publications.py no existe. Se omite.")

    run_step("[2/5] Actualizando GitHub", [sys.executable, "scripts/update_github.py"])
    run_step("[3/5] Actualizando Zenodo", [sys.executable, "scripts/update_zenodo.py"])
    run_step("[4/5] Unificando productos", [sys.executable, "scripts/update_products.py"])
    run_step(
        "[5/5] Construyendo MkDocs",
        [sys.executable, "-m", "mkdocs", "build", "--strict"],
    )

    print("\n" + "=" * 60)
    print(" Sitio unificado y actualizado correctamente.")
    print("=" * 60)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
