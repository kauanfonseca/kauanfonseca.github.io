# kauanfonseca.github.io

Personal research site built with [Quarto](https://quarto.org), R, Plotly,
Leaflet and Observable JS, published to GitHub Pages by GitHub Actions.

## Local setup

```bash
# 1. Quarto CLI (once): https://quarto.org/docs/get-started/
quarto check

# 2. R packages
Rscript R/00-bootstrap.R

# 3. Live preview at http://localhost:4200
quarto preview
```

## Publishing

1. Create a repository named `<your-username>.github.io` and push this folder
   to the `main` branch.
2. In **Settings > Pages**, set the source to **Deploy from a branch**,
   branch `gh-pages`, folder `/ (root)`.
3. Push to `main`. The workflow in `.github/workflows/publish.yml` renders the
   site and force-pushes the output to `gh-pages`.

The first run also creates the `gh-pages` branch. If you prefer to publish
from your own machine instead, run `quarto publish gh-pages` and delete the
workflow file.

## Caching (`_freeze/`)

`execute.freeze: auto` in `_quarto.yml` caches chunk output. Commit the
`_freeze/` directory: the runner then serves cached results and never needs R
installed, which makes builds fast and immune to package drift. If you commit
`_freeze/`, you can delete the three R setup steps in the workflow.

## Before you publish: what is real and what is not

This scaffold ships with placeholders and synthetic data so that it renders on
a clean machine. None of it should go live under your name unchecked.

| Item | Status |
|------|--------|
| `data/example_btc.csv` | **Synthetic.** Generated to demonstrate the BTC code path. Swap in a real event or keep it and leave the "synthetic input, real model" note in place. |
| `data/sites.csv` | **Empty.** Site codes only; fill in coordinates, width and discharge. The map hides itself until `lat`/`lon` exist. |
| `data/publications.csv` | Real entries, but check the status wording before it is public. |
| Diel oxygen figure | Forward model on synthetic input; labelled as such in a callout. |
| `references.bib` | Only the StreamLog Zenodo record. Paste real BibTeX from publishers or DOIs; do not let a placeholder citation reach the live site. |
| `cv.qmd` | Institutions, dates, advisor and service section are `CHANGE_ME`. |
| Email / Scholar / ORCID / Lattes | `example.org` and `CHANGE_ME` in `_quarto.yml` and `index.qmd`. |
| `images/profile.jpg`, `images/favicon.png` | Placeholder images. |
| `cv/kauan-fonseca-cv.pdf` | Missing; the CV page links to it. |

Fastest way to find everything left to edit:

```bash
grep -rn "CHANGE_ME\|example.org\|FILL IN" --include="*.qmd" --include="*.yml" .
```

## Files to replace before going live

| File | What to change |
|------|----------------|
| `_quarto.yml` | `site-url`, `repo-url`, email, GitHub handle |
| `index.qmd` | Scholar / ORCID / Lattes URLs, bio text |
| `images/profile.jpg` | Your photo (square, at least 600 px) |
| `images/favicon.png` | 64x64 icon |
| `research.qmd` | Real site coordinates in the `sites` tibble |
| `references.bib` | Your actual references |
| `cv.qmd` | Institutions, dates, advisor |
| `cv/kauan-fonseca-cv.pdf` | Your PDF CV |

## Adding a post

```bash
mkdir -p posts/2026-10-01-short-slug
$EDITOR posts/2026-10-01-short-slug/index.qmd
```

Give it `title`, `description`, `date`, `categories` and an `image` in the
YAML header; the listing on `posts/index.qmd` picks it up automatically.
