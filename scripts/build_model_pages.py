#!/usr/bin/env python3
"""Regenerate models/omni/index.html and models/transcribe/index.html.

models/index.html is the only page to edit by hand. The per-model pages are
copies of it with their own title, description and canonical URL, so each URL
works on any static host without server rewrites. The page's script reads the
path to pick which model is shown.

Run from the repo root after editing models/index.html:
    python3 scripts/build_model_pages.py
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent / "models"
BASE_URL = "https://missionforce.ai/models/"
OVERVIEW_TITLE = "SOV — Sovereign AI Voice Models from Salesforce"
OVERVIEW_DESCRIPTION = (
    "Introducing SOV-Omni-1 and SOV-Transcribe-1, sovereign AI voice models from "
    "Salesforce x Arcanum, benchmarked against leading voice models."
)

PAGES = {
    "omni": {
        "title": "SOV-Omni-1 — Sovereign AI Voice Model from Salesforce",
        "description": (
            "SOV-Omni-1, a sovereign AI voice model from Salesforce x Arcanum, "
            "benchmarked against leading voice models."
        ),
    },
    "transcribe": {
        "title": "SOV-Transcribe-1 — Sovereign AI Speech Recognition from Salesforce",
        "description": (
            "SOV-Transcribe-1, a sovereign AI speech recognition model from Salesforce "
            "x Arcanum, benchmarked against commercial and open-source models."
        ),
    },
}


def replace(html: str, old: str, new: str, count: int) -> str:
    found = html.count(old)
    if found != count:
        raise SystemExit(f"Expected {count} of {old!r} in models/index.html, found {found}")
    return html.replace(old, new)


def main() -> None:
    source = (ROOT / "index.html").read_text()
    split = source.index("</head>")
    source_head, body = source[:split], source[split:]  # only <head> metadata differs
    for slug, page in PAGES.items():
        url = f"{BASE_URL}{slug}/"
        head = source_head
        head = replace(head, OVERVIEW_TITLE, page["title"], 3)  # og:title, <title>, WebPage name
        head = replace(head, OVERVIEW_DESCRIPTION, page["description"], 3)
        head = replace(head, f'rel="canonical" href="{BASE_URL}"', f'rel="canonical" href="{url}"', 1)
        head = replace(head, f'property="og:url" content="{BASE_URL}"', f'property="og:url" content="{url}"', 1)
        head = replace(
            head,
            f'"@id": "{BASE_URL}#webpage",\n            "url": "{BASE_URL}"',
            f'"@id": "{url}#webpage",\n            "url": "{url}"',
            1,
        )
        html = head + body
        out = ROOT / slug / "index.html"
        out.parent.mkdir(exist_ok=True)
        out.write_text(
            html.replace("<!doctype html>", "<!doctype html>\n<!-- Generated from models/index.html by scripts/build_model_pages.py; edit that file instead. -->", 1)
        )
        print(f"wrote {out.relative_to(ROOT.parent)}")


if __name__ == "__main__":
    main()
