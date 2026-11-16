# SOV models site

Static pages for Salesforce's SOV voice models (SOV-Omni-1, SOV-Transcribe-1),
meant to be served at `https://missionforce.ai/models/`.

## Deploying to missionforce.ai

Copy the `models/` directory to the web root of missionforce.ai, so that
`models/index.html` is served at `/models/`. Nothing else in this repo is needed.

| URL                                    | File                            |
| -------------------------------------- | ------------------------------- |
| `https://missionforce.ai/models/`            | `models/index.html`             |
| `https://missionforce.ai/models/omni/`       | `models/omni/index.html`        |
| `https://missionforce.ai/models/transcribe/` | `models/transcribe/index.html`  |

- **No build step and no server rewrites.** Each URL is a real file, so any
  static host works (S3/CloudFront, nginx, Netlify, Vercel, GitHub Pages, ...).
  The host only needs to serve `index.html` for a directory URL, which they all
  do by default. Most hosts also redirect `/models/omni` to `/models/omni/`.
- **It must live at `/models/`.** Icons and the social image are referenced as
  `/models/...`, and canonical/Open Graph URLs point at
  `https://missionforce.ai/models/...`. To serve it elsewhere, search and replace
  those in `models/index.html` and `scripts/build_model_pages.py`, then regenerate.
- **External requests:** fonts load from Google Fonts. Everything else is in
  `models/`.

## How the model URLs work

The Omni / Transcribe picker on the page updates the URL
(`/models/omni/`, `/models/transcribe/`) without reloading, and back/forward
switch models. On load, the page reads its path to decide which model to show;
`/models/` shows Omni.

## Editing

Edit only `models/index.html`, then regenerate the per-model pages, which are
copies of it with their own title, description and canonical URL:

```sh
python3 scripts/build_model_pages.py
```

To preview locally, serve the repo root (not `models/`) so the `/models/` paths
resolve:

```sh
python3 -m http.server 8000   # then open http://localhost:8000/models/
```

To add a model, add its menu item and comparison panel to `models/index.html`,
add it to `slugs`/`titles` in the page script and to `PAGES` in
`scripts/build_model_pages.py`, then regenerate.

The root `index.html` only redirects to `/models/` for the GitHub Pages copy at
launa-model.github.io; it isn't needed on missionforce.ai.
