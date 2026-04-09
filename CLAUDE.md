# CLAUDE.md — AI Assistant Guide for quantum-plasmoid

This file provides context for AI assistants (Claude Code and similar tools) working in this repository.

---

## Project Overview

**quantum-plasmoid** is an interdisciplinary academic documentation and knowledge portal exploring consciousness, quantum physics, fractals, and complex systems. It is published as a static website via GitHub Pages and combines:

- A Three.js-animated web frontend (HTML/CSS/JS)
- Extensive research documentation in Markdown
- Embedded audio podcasts
- Interactive data visualizations (React/D3/TypeScript)
- Python utilities for content processing and link validation

The live site is served from the `docs/` directory on GitHub Pages.

---

## Repository Structure

```
quantum-plasmoid/
├── .github/workflows/          # CI/CD pipelines (pages, selenium, eleventy)
├── core-concepts/              # Theoretical foundations
│   ├── fractal-systems/        # Fractals across quantum/neural/cosmic scales
│   ├── quantum-dynamics/       # Plasmoid fields, qualia torii, cosmic tensegrity
│   ├── recursive-systems/      # Meta-theoretical recursion foundations
│   └── consciousness/          # Models of consciousness and semantic processing
├── theorems/                   # Major theoretical frameworks
│   ├── eigenmode-theory/       # Consciousness as stable eigenmode solutions
│   ├── orchard-theorem/        # ORCHARD computational framework
│   ├── zeta-correspondence/    # Riemann zeta ↔ consciousness correspondence
│   └── ray-dag/                # DAG models of mind-matter interaction
├── applications/               # Applied domains
│   ├── computational/          # AGI concepts, ruliad traversal
│   ├── health/                 # Health applications via recursive dynamics
│   └── integrative/            # Interdisciplinary extensions
├── time-models/                # Fractal time and CAP optimization models
├── visualizations/
│   └── eigenvalue-spiral/      # Standalone React/D3/TypeScript visualization
├── papers/                     # Research paper abstracts (5 papers)
├── docs/                       # Compiled static site (served by GitHub Pages)
│   ├── index.html              # Main landing page (522 lines)
│   ├── script.js               # Three.js canvas, carousels, podcast loader
│   ├── styles.css              # Full site CSS with animations (1178 lines)
│   └── _podcasts.json          # Metadata for 13 podcast audio files
├── github_math_cleanup.py      # LaTeX → Unicode conversion utility
├── test_github_math_cleanup.py # Unit tests for math cleanup utility
├── test_selenium_links.py      # Selenium browser automation link tests
├── run_tests.bat               # Windows test runner (Python tests)
├── requirements.txt            # Python scientific computing dependencies
├── package.json                # NPM config and build scripts
└── mathematicalFoundations.md  # Mathematical reference (root level)
```

---

## Technology Stack

| Layer | Technology |
|---|---|
| Frontend | HTML5, CSS3, vanilla JavaScript |
| 3D Graphics | Three.js (cosmic canvas background) |
| Visualization | React 18, D3.js, TypeScript (eigenvalue-spiral) |
| Build Tooling | Node.js / npm, `cpx`, `rimraf`, `npm-run-all` |
| Local Dev Server | `npx serve docs` |
| Python Utilities | Python 3.11+, unittest, Selenium |
| Scientific Python | numpy, scipy, pandas, sympy, torch, tensorflow, qutip, pennylane |
| CI/CD | GitHub Actions → GitHub Pages |

---

## Development Workflows

### Local Development

```bash
npm start          # Serves docs/ on http://localhost:3000
```

All content to be served is in `docs/`. Edit HTML/CSS/JS there directly for frontend changes. For content changes, edit the source Markdown in the subdirectories.

### Build Pipeline

```bash
npm run build      # clean → cpx docs/**/* to dist/ → create dist/.nojekyll
npm run deploy     # cpx dist/**/* back to docs/
```

The build pipeline is intentionally simple — it copies `docs/` to `dist/` and back. There is no SSG (Hugo, 11ty, etc.) generating HTML from Markdown; HTML pages are authored directly in `docs/`.

### Python Utilities

```bash
python github_math_cleanup.py       # Convert LaTeX math to Unicode in markdown files
python test_github_math_cleanup.py  # Run math cleanup unit tests
python test_selenium_links.py       # Run browser link validation (requires Chrome)
```

### NPM Scripts Summary

| Script | Command | Purpose |
|---|---|---|
| `npm start` | `npx serve docs` | Local dev server |
| `npm run build` | clean + copy | Prepare dist/ |
| `npm run clean` | `rimraf dist` | Remove dist/ |
| `npm run build:docs` | `cpx "docs/**/*" dist` | Copy docs to dist |
| `npm run deploy` | `cpx "dist/**/*" docs` | Deploy dist to docs |
| `npm run postbuild` | creates `.nojekyll` | Prevents Jekyll on Pages |

---

## CI/CD Pipelines

Three GitHub Actions workflows in `.github/workflows/`:

### `pages.yml` — Main Deployment
- **Triggers:** push to `main`
- **Steps:** checkout → cache npm → Node 20 → `npm ci` → `npm run build` → verify build → copy to `docs/` → commit & push → deploy to GitHub Pages
- **Bot commits** use `GITHUB_TOKEN` with `github-actions[bot]` identity

### `selenium-links.yml` — Link Validation
- **Triggers:** push to `main`, PR to `main`
- **Runs:** headless Chrome Selenium tests against the deployed site
- Tests navigation links, anchor links, and viewport visibility

### `eleventy-build.yml` — Eleventy (Partially Configured)
- Node 20 + npm ci + build to `_site/`
- Deploy steps are commented out — not currently active

---

## Content Architecture

### Podcast System
- Audio metadata centralized in `docs/_podcasts.json` (13 files across 4 sections)
- `docs/script.js` fetches this JSON and renders audio players dynamically
- Each major section (theorems, applications, core-concepts) has an associated `.mp3`

### Section Pattern
Every major content section follows this structure:
```
section-name/
├── README.md          # Overview of this section
├── subsection-a/
│   └── content.md     # Source markdown (not auto-compiled)
└── ...
```
Corresponding compiled pages live under `docs/section-name/`.

### Mathematical Content
- `github_math_cleanup.py` converts LaTeX notation (`\[...\]`, `$...$`, `$$...$$`) to Unicode symbols
- Generates `.diff` files for review before applying changes
- Key conversions: subscripts, Greek letters, mathematical operators

---

## Naming Conventions

| Context | Convention | Example |
|---|---|---|
| Directories | kebab-case | `core-concepts/`, `eigenmode-theory/` |
| Content file titles | PascalCase or Title Case | `MATHEMATICAL_FOUNDATIONS.md` |
| CSS classes | kebab-case | `.nav-links`, `.principle-card` |
| JavaScript functions | camelCase | `initCosmicCanvas()`, `setupTheoremCarousel()` |
| JavaScript variables | camelCase | `podcasts`, `currentSlide` |
| Math symbols in content | Unicode preferred | `Ψ`, `ζ`, `⊕`, `ℂ` |

---

## Key Files to Know

| File | Purpose |
|---|---|
| `docs/index.html` | Main landing page — all navigation anchors, section layout |
| `docs/script.js` | All interactive behavior: Three.js canvas, carousels, podcast loader, dropdowns |
| `docs/styles.css` | Complete site styling including animations and responsive design |
| `docs/_podcasts.json` | Single source of truth for podcast metadata |
| `github_math_cleanup.py` | LaTeX-to-Unicode conversion utility |
| `visualizations/eigenvalue-spiral/` | Standalone React/D3/TS project with its own `package.json` |
| `requirements.txt` | Python environment for scientific computing and testing |
| `package.json` | Root NPM config — defines all build/dev scripts |

---

## Testing

### Python Unit Tests (`test_github_math_cleanup.py`)
- Uses `unittest` (not pytest)
- Tests LaTeX → Unicode conversion functions
- Compares backup files against converted output
- Run: `python test_github_math_cleanup.py`

### Browser/Link Tests (`test_selenium_links.py`)
- Uses Selenium + Chrome (headless in CI)
- Tests navigation links, anchor scrolling, viewport visibility
- Requires Chrome installed locally; in CI uses `webdriver-manager`
- Run: `python test_selenium_links.py`

### No npm-level tests
`npm test` is not configured — it prints "No tests specified" and exits 1.

---

## Python Environment

Install dependencies:
```bash
pip install -r requirements.txt
```

Notable package groups:
- **Quantum:** `qutip`, `pennylane`
- **ML/DL:** `torch`, `tensorflow`, `scikit-learn`
- **TDA:** `ripser`, `persim`, `gudhi`
- **Signal:** `spectrum`, `pywavelets`, `mne`
- **Fractional calculus:** `torchfde`, `pyfod` (installed from git)
- **Geometry:** `pymanopt`, `geomstats`
- **Network:** `networkx`, `pyunicorn`

---

## Important Constraints & Conventions

1. **docs/ is the served artifact.** Do not delete or restructure `docs/` — GitHub Pages serves from there. Changes to `docs/` go live on push to `main` after the CI pipeline runs.

2. **Source Markdown is not auto-compiled.** HTML pages in `docs/` are hand-authored. If you update a `.md` file in `core-concepts/` or `theorems/`, the corresponding `docs/` HTML must be updated separately.

3. **No Jekyll.** A `.nojekyll` file in `docs/` prevents GitHub from running Jekyll. Do not remove it.

4. **Visualizations have their own package.json.** The `visualizations/eigenvalue-spiral/` project is a separate npm workspace. Run `npm install` inside it separately if working on it.

5. **Math notation:** Prefer Unicode over raw LaTeX in markdown content. Use `github_math_cleanup.py` to convert existing LaTeX.

6. **Podcast JSON is the single source of truth.** Do not hardcode podcast paths in HTML — update `docs/_podcasts.json` instead, as `script.js` reads it dynamically.

7. **Bot commits in CI.** The `pages.yml` workflow makes automated commits back to `main`. When checking git history, these are authored by `github-actions[bot]`.

---

## Branch Strategy

- `main` — production branch; pushes trigger auto-deployment to GitHub Pages
- Feature work should be done on feature branches and PRged to `main`
- The CI Selenium tests run on PRs to `main` as a gate

---

## Known Gaps / Tooling Notes

- No linting configuration (no ESLint, no Prettier, no flake8 config)
- No Docker support
- Eleventy workflow exists but deploy is disabled — do not assume 11ty is the build system
- `npm test` is not wired up — run Python tests directly
- No API layer — this is a purely static site
