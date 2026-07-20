# SportsLabResearch automatic updater

## Instalación local

```powershell
py -m pip install requests beautifulsoup4
```

## Ejecución

```powershell
py .\scripts\update_site.py
```

Genera:

- `docs/publications.md`
- `docs/software.md`
- `docs/zenodo.md`

## Automatización en GitHub

El workflow `.github/workflows/update-site.yml` se ejecuta cada día y también
puede iniciarse manualmente desde la pestaña **Actions**.

## Menú MkDocs

Añade al `nav` de `mkdocs.yml`:

```yaml
  - Publications: publications.md
  - Software: software.md
  - Zenodo: zenodo.md
```
