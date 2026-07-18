---
hide:
  - navigation
  - toc
  - footer
title: SportsLabResearch
---

<style>
.md-header,
.md-tabs,
.md-sidebar,
.md-footer {
  display: none !important;
}

.md-main,
.md-main__inner,
.md-content,
.md-content__inner {
  width: 100% !important;
  max-width: none !important;
  margin: 0 !important;
  padding: 0 !important;
}

.md-content__inner::before {
  display: none !important;
}

.slr-page {
  width: 100%;
  margin: 0;
  overflow-x: hidden;
  font-family: Arial, Helvetica, sans-serif;
}

/* MENÚ REAL Y FUNCIONAL */

.slr-menu {
  position: fixed;
  top: 0;
  left: 0;
  z-index: 9999;
  display: flex;
  align-items: center;
  justify-content: space-between;
  width: 100%;
  height: 86px;
  padding: 0 4.5%;
  box-sizing: border-box;
  background: rgba(1, 10, 24, 0.97);
  border-bottom: 1px solid rgba(255,255,255,0.12);
}

.slr-logo {
  color: #fff !important;
  font-size: 28px;
  font-weight: 800;
  letter-spacing: -1px;
  text-decoration: none !important;
}

.slr-logo span {
  color: #167cff;
}

.slr-menu-links {
  display: flex;
  align-items: center;
  gap: 34px;
}

.slr-menu-links a {
  position: relative;
  color: #fff !important;
  font-size: 16px;
  font-weight: 700;
  text-decoration: none !important;
}

.slr-menu-links a:hover {
  color: #1683ff !important;
}

.slr-menu-links a:first-child::after {
  content: "";
  position: absolute;
  left: 0;
  right: 0;
  bottom: -17px;
  height: 3px;
  background: #1683ff;
}

/* PORTADA */

.slr-hero {
  position: relative;
  width: 100%;
  height: 100vh;
  min-height: 680px;
  margin-top: 0;
  overflow: hidden;
  background: #020b1c;
}

.slr-hero-image {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: calc(100% + 100px);
  object-fit: cover;
  object-position: center top;
  transform: translateY(-84px);
}

/* MENSAJE PRINCIPAL DE PORTADA */

.slr-hero-copy {
  position: absolute;
  left: 4.4%;
  bottom: 28%;
  z-index: 20;
  width: min(760px, 88%);
  color: #fff;
}

.slr-eyebrow {
  margin: 0 0 14px;
  color: #5ba7ff;
  font-size: 15px;
  font-weight: 800;
  letter-spacing: 0.08em;
  text-transform: uppercase;
}

.slr-hero-copy h1 {
  max-width: 760px;
  margin: 0;
  color: #fff;
  font-size: clamp(38px, 5vw, 68px);
  font-weight: 800;
  line-height: 1.05;
  letter-spacing: -0.03em;
}

.slr-hero-text {
  max-width: 650px;
  margin: 22px 0 0;
  color: rgba(255, 255, 255, 0.86);
  font-size: 19px;
  line-height: 1.55;
}

/* BOTONES FUNCIONALES */

.slr-actions {
  position: absolute;
  left: 4.4%;
  bottom: 12%;
  z-index: 20;
  display: flex;
  gap: 18px;
}

.slr-button {
  display: inline-flex;
  align-items: center;
  gap: 18px;
  padding: 15px 24px;
  border: 1px solid rgba(255,255,255,0.7);
  border-radius: 6px;
  color: #fff !important;
  font-size: 16px;
  font-weight: 700;
  text-decoration: none !important;
  background: rgba(1,8,20,0.68);
}

.slr-button-primary {
  border-color: #087cff;
  background: #087cff;
}

.slr-button:hover {
  background: #1683ff;
  border-color: #1683ff;
}

/* ECOSISTEMA */

.slr-ecosystem {
  width: 100%;
  box-sizing: border-box;
  padding: 52px 5% 80px;
  background: #fff;
  color: #10192d;
}

.slr-ecosystem h1 {
  margin: 0;
  color: #10192d;
  text-align: center;
  font-size: clamp(32px, 4vw, 48px);
  font-weight: 800;
}

.slr-title-line {
  width: 48px;
  height: 4px;
  margin: 18px auto 48px;
  background: #087cff;
}

.slr-cards {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 42px;
  width: 100%;
  max-width: 1450px;
  margin: auto;
}

.slr-card {
  display: block;
  padding: 16px 20px 24px;
  color: #10192d !important;
  text-decoration: none !important;
  border-bottom: 3px solid transparent;
  transition: transform .2s ease, border-color .2s ease;
}

.slr-card:hover {
  transform: translateY(-5px);
  border-color: #087cff;
}

.slr-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 62px;
  height: 62px;
  margin-bottom: 22px;
  border: 2px solid #087cff;
  border-radius: 50%;
  color: #087cff;
  font-size: 29px;
  font-weight: 700;
}

.slr-card h2 {
  margin: 0 0 13px;
  color: #10192d;
  font-size: 21px;
  font-weight: 800;
}

.slr-card p {
  min-height: 100px;
  margin: 0 0 16px;
  color: #26344b;
  font-size: 16px;
  line-height: 1.55;
}

.slr-link {
  color: #087cff;
  font-weight: 700;
}

/* RESPONSIVE */

@media screen and (max-width: 1050px) {
  .slr-menu-links {
    gap: 18px;
  }

  .slr-menu-links a {
    font-size: 14px;
  }

  .slr-cards {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media screen and (max-width: 760px) {
  .slr-menu {
    height: 70px;
    padding: 0 20px;
  }

  .slr-logo {
    font-size: 22px;
  }

  .slr-menu-links {
    display: none;
  }

  .slr-hero {
    height: 78vh;
    min-height: 540px;
  }

  .slr-hero-image {
    height: calc(100% + 80px);
    object-position: 61% top;
    transform: translateY(-65px);
  }


  .slr-hero-copy {
    left: 20px;
    right: 20px;
    bottom: 190px;
    width: auto;
  }

  .slr-eyebrow {
    font-size: 12px;
  }

  .slr-hero-copy h1 {
    font-size: 34px;
  }

  .slr-hero-text {
    margin-top: 16px;
    font-size: 16px;
  }
  .slr-actions {
    left: 20px;
    right: 20px;
    bottom: 28px;
    flex-direction: column;
  }

  .slr-button {
    justify-content: center;
  }

  .slr-cards {
    grid-template-columns: 1fr;
    gap: 12px;
  }

  .slr-card p {
    min-height: auto;
  }
}
</style>

<div class="slr-page">

  <nav class="slr-menu">
    <a class="slr-logo" href="./">
      SportsLab<span>Research</span>
    </a>

    <div class="slr-menu-links">
      <a href="./">Home</a>
      <a href="about/">About</a>
      <a href="portfolio/">Portfolio</a>
      <a href="framework/">Framework</a>
      <a href="standards/">Standards</a>
      <a href="publications/">Publications</a>
      <a href="contact/">Contact</a>
    </div>
  </nav>

  <section class="slr-hero">
    <img
      class="slr-hero-image"
      src="assets/portada.png"
      alt="SportsLabResearch">

    <div class="slr-hero-copy">
      <p class="slr-eyebrow">
        Open Research Software for Sports Science
      </p>

      <h1>
        Scientific software, wearable technologies and reproducible research.
      </h1>

      <p class="slr-hero-text">
        SportsLabResearch develops open-source tools, validated workflows and
        research infrastructure for sports science.
      </p>
    </div>

    <div class="slr-actions">
      <a class="slr-button slr-button-primary" href="portfolio/">
        Explore Portfolio →
      </a>

      <a class="slr-button" href="framework/">
        Learn More →
      </a>
    </div>
  </section>

  <section class="slr-ecosystem">

    <h1>Research Ecosystem</h1>
    <div class="slr-title-line"></div>

    <div class="slr-cards">

      <a class="slr-card" href="portfolio/">
        <div class="slr-icon">↗</div>
        <h2>Research Software</h2>
        <p>
          Aplicaciones científicas para procesamiento, análisis,
          visualización e informes.
        </p>
        <span class="slr-link">Ver portfolio →</span>
      </a>

      <a class="slr-card" href="about/">
        <div class="slr-icon">⌚</div>
        <h2>Wearable Technologies</h2>
        <p>
          Frecuencia cardiaca, HRV, GNSS, IMU y monitorización
          fisiológica.
        </p>
        <span class="slr-link">Ver áreas →</span>
      </a>

      <a class="slr-card" href="framework/">
        <div class="slr-icon">AI</div>
        <h2>Artificial Intelligence</h2>
        <p>
          Machine learning, visión artificial y análisis inteligente
          aplicado al deporte.
        </p>
        <span class="slr-link">Ver framework →</span>
      </a>

      <a class="slr-card" href="portfolio/">
        <div class="slr-icon">▦</div>
        <h2>Embedded Systems</h2>
        <p>
          Arduino, sensores conectados y hardware experimental para
          investigación.
        </p>
        <span class="slr-link">Ver proyectos →</span>
      </a>

    </div>
  </section>

</div>


