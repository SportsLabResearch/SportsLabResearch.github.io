$ErrorActionPreference = "Stop"

$root = Get-Location
$docs = Join-Path $root "docs"
$styles = Join-Path $docs "stylesheets"
$images = Join-Path $docs "assets\images"
$mkdocs = Join-Path $root "mkdocs.yml"
$index = Join-Path $docs "index.md"
$css = Join-Path $styles "home.css"

if (-not (Test-Path $mkdocs)) {
    throw "No se encuentra mkdocs.yml. Ejecuta este script desde la raíz del proyecto."
}

New-Item -ItemType Directory -Force $styles | Out-Null

$logoCandidates = @(
    (Join-Path $images "logo-header.png"),
    (Join-Path $images "logo-sportslabresearch.png"),
    (Join-Path $images "Logo_fina_02.png"),
    (Join-Path $images "logo.png")
)

$logoPath = $logoCandidates | Where-Object { Test-Path $_ } | Select-Object -First 1

if (-not $logoPath) {
    throw "No se ha encontrado el logo en docs\assets\images."
}

$logoRelative = $logoPath.Substring($docs.Length + 1).Replace("\", "/")

$indexContent = @'
---
hide:
  - navigation
  - toc
---

<div class="slr-home">

<section class="slr-hero">
  <div class="slr-hero__content">
    <p class="slr-eyebrow">SCIENCE · DATA · INNOVATION</p>
    <h1>Open Scientific Software for Sport and Health Sciences</h1>
    <p class="slr-lead">
      Transforming scientific knowledge into reproducible software,
      validated methodologies and practical tools for research,
      education and professional practice.
    </p>

    <div class="slr-actions">
      <a class="slr-btn slr-btn--primary" href="products/">Explore Products</a>
      <a class="slr-btn" href="research/">Research</a>
      <a class="slr-btn" href="publications/">Publications</a>
    </div>

    <div class="slr-contact-strip">
      <strong>Research collaboration</strong>
      <a href="contact/">pepepinoortega@gmail.com</a>
    </div>
  </div>

  <div class="slr-hero__visual">
    <img src="__LOGO__" alt="SportsLabResearch">
  </div>
</section>

<section class="slr-workflow">
  <div><strong>Research</strong><span>Scientific questions and real needs</span></div>
  <div><strong>Software</strong><span>Robust and reproducible tools</span></div>
  <div><strong>Validation</strong><span>Methodological and technical validation</span></div>
  <div><strong>Impact</strong><span>Knowledge transfer and real-world use</span></div>
</section>

<section class="slr-featured">
  <div class="slr-featured__visual">
    <div class="slr-screen">
      <div class="slr-screen__bar"></div>
      <div class="slr-screen__chart"></div>
      <div class="slr-screen__rows"></div>
    </div>
  </div>

  <div class="slr-featured__content">
    <span class="slr-kicker">FEATURED PRODUCT</span>
    <h2>SportsLabResearch-WIMU-DataExtractor</h2>
    <p>
      Scientific software for extracting, processing and validating WIMU® data.
      It supports automated file processing, comparison with SPRO and generation
      of Excel and Word reports.
    </p>
    <p><strong>Version:</strong> v1.0.2 &nbsp; · &nbsp; <strong>DOI:</strong> 10.5281/zenodo.21344653</p>
    <div class="slr-actions">
      <a class="slr-btn slr-btn--primary" href="https://github.com/SportsLabResearch/SportsLabResearch-WIMU-DataExtractor">GitHub</a>
      <a class="slr-btn" href="https://sportslabresearch.github.io/SportsLabResearch-WIMU-DataExtractor/">Documentation</a>
      <a class="slr-btn" href="https://zenodo.org/records/21344653">Zenodo</a>
    </div>
  </div>
</section>

<section>
  <div class="slr-section-title">
    <div>
      <span class="slr-kicker">PRODUCTS</span>
      <h2>Scientific Products</h2>
    </div>
    <a href="products/">View all products →</a>
  </div>

  <div class="slr-products">
    <article>
      <span class="slr-product-mark">BP</span>
      <h3>BloodPressure Analyzer</h3>
      <p>Blood-pressure classification, longitudinal monitoring and automated clinical reporting.</p>
      <a href="https://github.com/SportsLabResearch/SportsLabResearch-BloodPressure-Analyzer">GitHub →</a>
    </article>

    <article>
      <span class="slr-product-mark">HRV</span>
      <h3>HRV Longitudinal Analyzer</h3>
      <p>Longitudinal analysis of heart-rate variability for research, monitoring and education.</p>
      <a href="https://github.com/ppo1968/HRV-Longitudinal-Analyzer">GitHub →</a>
    </article>

    <article>
      <span class="slr-product-mark">BC</span>
      <h3>BreastCancer Wellbeing Analyzer</h3>
      <p>Analysis of wellbeing, sleep, fatigue, stress, pain and health variables.</p>
      <a href="research/">Research →</a>
    </article>

    <article>
      <span class="slr-product-mark">FIFA</span>
      <h3>FIFA World Cup 2026 Analyzer</h3>
      <p>Analysis of players, teams, matches and performance indicators.</p>
      <a href="https://github.com/SportsLabResearch/SportsLabResearch-Analytics-FIFA-WorldCup-2026-Analyzer">GitHub →</a>
    </article>
  </div>
</section>

<section class="slr-research">
  <div class="slr-section-title">
    <div>
      <span class="slr-kicker">RESEARCH</span>
      <h2>Research Areas</h2>
    </div>
    <a href="research/">Explore research →</a>
  </div>

  <div class="slr-research-grid">
    <span>Sport Performance</span>
    <span>Wearable Technology</span>
    <span>Physiological Monitoring</span>
    <span>Exercise and Health</span>
    <span>Artificial Intelligence</span>
    <span>Data Science</span>
  </div>
</section>

<section class="slr-bottom-grid">
  <article>
    <span class="slr-kicker">PUBLICATIONS</span>
    <h2>Latest Publications</h2>
    <p>Scientific output synchronized automatically from the University of Murcia research profile.</p>
    <a class="slr-btn" href="publications/">View publications</a>
  </article>

  <article class="slr-collab">
    <span class="slr-kicker">COLLABORATION</span>
    <h2>Collaborate with SportsLabResearch</h2>
    <p>Research projects · Scientific software · Technology validation · Data analysis · Education</p>
    <p><strong>José Pino-Ortega</strong><br>Faculty of Sport Sciences · University of Murcia</p>
    <a class="slr-btn slr-btn--primary" href="contact/">Contact</a>
    <a class="slr-btn" href="services/">Scientific Services</a>
  </article>
</section>

</div>
'@

$indexContent = $indexContent.Replace("__LOGO__", $logoRelative)
Set-Content -Path $index -Value $indexContent -Encoding UTF8

$cssContent = @'
:root {
  --slr-navy: #061829;
  --slr-navy-2: #0b2b43;
  --slr-blue: #0b66e4;
  --slr-cyan: #12c7d9;
  --slr-ink: #0c2740;
  --slr-muted: #5f7182;
  --slr-line: #d9e4ec;
  --slr-soft: #f4f8fb;
}

.md-main__inner {
  margin-top: 0;
}

.md-content__inner {
  max-width: none;
  margin: 0;
  padding: 0;
}

.md-content__inner > h1 {
  display: none;
}

.slr-home {
  color: var(--slr-ink);
  background: #fff;
}

.slr-home section {
  max-width: 1240px;
  margin: 0 auto;
  padding: 3.5rem 2rem;
}

.slr-hero {
  display: grid;
  grid-template-columns: 1.15fr .85fr;
  align-items: center;
  gap: 2rem;
  max-width: none !important;
  min-height: 520px;
  padding: 4.5rem max(2rem, calc((100vw - 1240px) / 2)) !important;
  color: #fff;
  background:
    radial-gradient(circle at 80% 35%, rgba(18,199,217,.28), transparent 34%),
    linear-gradient(120deg, #061829 0%, #07355b 58%, #0a8797 100%);
}

.slr-eyebrow,
.slr-kicker {
  display: inline-block;
  color: var(--slr-cyan);
  font-size: .72rem;
  font-weight: 800;
  letter-spacing: .12em;
}

.slr-hero h1 {
  max-width: 760px;
  margin: .8rem 0 1.2rem;
  color: #fff;
  font-size: clamp(2.3rem, 5vw, 4.4rem);
  line-height: 1.05;
  letter-spacing: -.04em;
}

.slr-lead {
  max-width: 680px;
  color: rgba(255,255,255,.84);
  font-size: 1.15rem;
  line-height: 1.75;
}

.slr-hero__visual {
  display: flex;
  align-items: center;
  justify-content: center;
}

.slr-hero__visual img {
  width: min(420px, 85%);
  opacity: .9;
  filter: drop-shadow(0 20px 45px rgba(0,0,0,.28));
}

.slr-actions {
  display: flex;
  flex-wrap: wrap;
  gap: .7rem;
  margin-top: 1.7rem;
}

.slr-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-height: 44px;
  padding: .7rem 1.15rem;
  color: inherit !important;
  font-weight: 750;
  text-decoration: none;
  border: 1px solid currentColor;
  border-radius: 7px;
}

.slr-btn--primary {
  color: #fff !important;
  background: linear-gradient(90deg, var(--slr-blue), var(--slr-cyan));
  border-color: transparent;
}

.slr-contact-strip {
  display: inline-flex;
  flex-wrap: wrap;
  gap: .8rem;
  margin-top: 2rem;
  padding: .8rem 1rem;
  border: 1px solid rgba(255,255,255,.2);
  border-radius: 8px;
  background: rgba(0,0,0,.13);
}

.slr-contact-strip a {
  color: var(--slr-cyan);
}

.slr-workflow {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 1rem;
  margin-top: -38px !important;
  padding-top: 0 !important;
}

.slr-workflow > div {
  padding: 1.25rem;
  background: #fff;
  border: 1px solid var(--slr-line);
  border-radius: 10px;
  box-shadow: 0 10px 30px rgba(8,36,61,.08);
}

.slr-workflow strong,
.slr-workflow span {
  display: block;
}

.slr-workflow span {
  margin-top: .3rem;
  color: var(--slr-muted);
  font-size: .85rem;
}

.slr-featured {
  display: grid;
  grid-template-columns: 1fr 1.15fr;
  align-items: center;
  gap: 2.5rem;
  margin-top: 1rem !important;
  background: var(--slr-soft);
  border: 1px solid var(--slr-line);
  border-radius: 14px;
}

.slr-featured h2,
.slr-section-title h2,
.slr-bottom-grid h2 {
  margin: .35rem 0 .8rem;
  color: var(--slr-ink);
}

.slr-screen {
  overflow: hidden;
  min-height: 290px;
  padding: 1.2rem;
  background: #0b2238;
  border-radius: 12px;
  box-shadow: 0 18px 40px rgba(6,24,41,.2);
}

.slr-screen__bar {
  height: 28px;
  margin-bottom: 1rem;
  background: linear-gradient(90deg, #143957 40%, #1e89a1 40%);
  border-radius: 6px;
}

.slr-screen__chart {
  height: 120px;
  background:
    linear-gradient(135deg, transparent 49%, #12c7d9 50%, transparent 51%) 0 0/28px 28px,
    #fff;
  border-radius: 8px;
}

.slr-screen__rows {
  height: 85px;
  margin-top: 1rem;
  background: repeating-linear-gradient(#fff 0 14px, #e7eef3 14px 16px);
  border-radius: 8px;
}

.slr-section-title {
  display: flex;
  align-items: end;
  justify-content: space-between;
  gap: 1rem;
}

.slr-section-title a {
  font-weight: 700;
}

.slr-products {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 1rem;
}

.slr-products article,
.slr-bottom-grid article {
  padding: 1.35rem;
  background: #fff;
  border: 1px solid var(--slr-line);
  border-radius: 10px;
}

.slr-products h3 {
  margin: .8rem 0 .5rem;
  color: var(--slr-ink);
  font-size: 1rem;
}

.slr-products p,
.slr-bottom-grid p {
  color: var(--slr-muted);
  font-size: .9rem;
}

.slr-product-mark {
  display: inline-flex;
  min-width: 48px;
  min-height: 48px;
  align-items: center;
  justify-content: center;
  padding: .45rem;
  color: #fff;
  font-size: .75rem;
  font-weight: 850;
  background: linear-gradient(135deg, var(--slr-blue), var(--slr-cyan));
  border-radius: 10px;
}

.slr-research {
  padding-top: 2rem !important;
}

.slr-research-grid {
  display: grid;
  grid-template-columns: repeat(6, 1fr);
  gap: .8rem;
}

.slr-research-grid span {
  padding: 1rem;
  text-align: center;
  font-size: .84rem;
  font-weight: 750;
  border-top: 3px solid var(--slr-blue);
  background: var(--slr-soft);
}

.slr-bottom-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
  padding-top: 1rem !important;
}

.slr-collab {
  background: linear-gradient(135deg, #eefaff, #fff) !important;
}

@media (max-width: 900px) {
  .slr-hero,
  .slr-featured,
  .slr-bottom-grid {
    grid-template-columns: 1fr;
  }

  .slr-hero__visual {
    order: -1;
  }

  .slr-hero__visual img {
    width: 220px;
  }

  .slr-workflow,
  .slr-products,
  .slr-research-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 560px) {
  .slr-home section {
    padding: 2.5rem 1rem;
  }

  .slr-workflow,
  .slr-products,
  .slr-research-grid {
    grid-template-columns: 1fr;
  }

  .slr-hero {
    padding: 3rem 1rem !important;
  }

  .slr-contact-strip {
    display: flex;
  }
}
'@

Set-Content -Path $css -Value $cssContent -Encoding UTF8

$mk = Get-Content $mkdocs -Raw

if ($mk -notmatch '(?m)^\s*-\s*stylesheets/home\.css\s*$') {
    if ($mk -match '(?m)^extra_css:\s*$') {
        $mk = $mk -replace '(?m)^extra_css:\s*$', "extra_css:`r`n  - stylesheets/home.css"
    }
    else {
        $mk += "`r`nextra_css:`r`n  - stylesheets/home.css`r`n"
    }

    Set-Content -Path $mkdocs -Value $mk -Encoding UTF8
}

Write-Host ""
Write-Host "Home profesional implementada correctamente." -ForegroundColor Green
Write-Host "Ejecuta: py -m mkdocs serve" -ForegroundColor Cyan
