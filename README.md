# flipper
SDSS splash page generator for data release websites

[![Run Tests](https://github.com/sdss/flipper/actions/workflows/test.yml/badge.svg)](https://github.com/sdss/flipper/actions/workflows/test.yml)

This project provides the main SDSS splash page at **[release].sdss.org**, e.g. https://dr20.sdss.org/. It includes tools to build the static HTML page and generate the visual snapshots used on the page.


## Overview

Two CLI tools are provided:

- `flipper` — builds the static HTML splash page  
- `flipper_snapshot` — generates screenshot snapshots (requires Playwright)

`flipper_snapshot` is typically run locally, as it depends on Playwright browsers. The resulting plots can then be committed to the repository or deployed to the server.

## Installation

Using `uv` (recommended):

```bash
uv sync
```

Install with development dependencies:

```bash
uv sync --group dev
```

Install with snapshot dependencies (requires Playwright):

```bash
uv sync --group snap
```

Then install Playwright browsers:

```bash
playwright install
```

> Note: Snapshot generation requires the `snap` dependency group. Development tools require the `dev` group.

## Usage

### Build the splash page

```bash
flipper [options]
```

Options:

- `-r`, `--release` — manually set the release (e.g. `dr19`)
- `-t`, `--dev` — use testing base URL for WordPress
- `-j`, `--skyserver` — use SkyServer without release
- `-m`, `--mirror` — use mirror URL (e.g. `dev-mirror` for `dev-mirror.sdss.org`)

Example:

```bash
flipper --release dr19
```

### Generate snapshots

```bash
flipper_snapshot [options]
```

Options:

- `--yaml` — path to YAML file containing snapshot configuration
- `--outdir` — output directory for generated images

Example:

```bash
flipper_snapshot --yaml snapshots.yml --outdir ./images
```

Run this locally if Playwright is not available on the server. Commit or deploy the generated images after running.

## Development

Run tests:

```bash
pytest
```

## Deployment

Typical workflow:

1. Generate snapshots locally (if needed):
   ```bash
   flipper_snapshot --yaml snapshots.yml --outdir ./images
   ```
2. Commit updated plots to the repository  
3. Build the page:
   ```bash
   flipper --release dr17
   ```
4. Deploy the generated static files to the server