# SportsLabResearch unified version

This version simplifies the public website:

- **Home** provides only a concise entry point.
- **Products** unifies GitHub repositories, releases, documentation and Zenodo DOI.
- **Research** presents research lines and related applications.
- **Publications** contains only scientific publications synchronized from UMU.
- Separate **Software** and **Zenodo** menu pages are removed.
- A single GitHub Pages workflow updates and deploys the site.

Local test:

```powershell
py -m pip install -r requirements.txt
py .\scripts\update_site.py
py -m mkdocs serve
```
