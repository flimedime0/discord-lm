#!/usr/bin/env python
"""
Rebuild PROJECT_STATE.md from GitHub Issues.

Convention:
* Each issue title starts with canonical Task ID, e.g. "dockerize-13: Docker & Compose".
* One of these labels is present: status:todo | status:in-progress | status:done
"""
import os
import requests  # type: ignore[import]
import pathlib
import datetime

REPO = "flimedime0/discord-lm-app"
TOKEN = os.environ["GH_TOKEN"]
HEADERS = {"Authorization": f"Bearer {TOKEN}"}


def fetch_issues():
    q = f"repo:{REPO} is:issue label:Task-ID"
    res = requests.get(
        "https://api.github.com/search/issues",
        headers=HEADERS,
        params={"q": q, "per_page": 100},
        timeout=20,
    )
    res.raise_for_status()
    return res.json()["items"]


buckets: dict[str, list[str]] = {"in-progress": [], "todo": [], "done": []}
for it in fetch_issues():
    status = next(
        (
            lbl_obj["name"].split(":", 1)[1]
            for lbl_obj in it["labels"]
            if lbl_obj["name"].startswith("status:")
        ),
        "todo",
    )
    buckets[status].append(it["title"])

parts = ["## Project road-map  *(auto-generated)*\n"]
for sec in ("in-progress", "todo", "done"):
    parts.append(f"### {sec.replace('-', ' ').title()}")
    for title in sorted(buckets[sec]):
        parts.append(f"- {title}")
    parts.append("")
pathlib.Path("PROJECT_STATE.md").write_text("\n".join(parts))
print("PROJECT_STATE.md regenerated at", datetime.datetime.utcnow())
