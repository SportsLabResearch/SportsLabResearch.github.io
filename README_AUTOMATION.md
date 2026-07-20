# SportsLabResearch automatic updater

The website uses a single GitHub Actions workflow:

- `.github/workflows/pages.yml`

It runs on every push to `main`, once per day, and manually from **Actions**.

The workflow performs the full process in one job:

1. Updates publications from UMU.
2. Updates repositories and releases from GitHub.
3. Updates records and DOI from Zenodo.
4. Builds MkDocs with strict validation.
5. Commits the generated Markdown pages when they change.
6. Deploys the already-generated `site/` directory directly to GitHub Pages.

## Local execution

```powershell
py -m pip install -r requirements.txt
py .\scripts\update_site.py
```

Generated pages:

- `docs/publications.md`
- `docs/software.md`
- `docs/zenodo.md`
