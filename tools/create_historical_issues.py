import re
import subprocess
import pathlib

REPO = "flimedime0/discord-lm-app"

KEYWORDS = [
    "dockerize",
    "mypy",
    "coverage",
    "dependabot",
    "release",
    "logging",
    "docs-mkdocs",
    "splitter",
    "ci-fix",
]


def parse_changelog():
    lines = pathlib.Path("CHANGELOG.md").read_text().splitlines()
    sections = {"Unreleased": [], "0.1.0": []}
    current_block = None
    capture = False
    for line in lines:
        if line.startswith("## [Unreleased]"):
            current_block = "Unreleased"
            capture = False
            continue
        if re.match(r"## \[0\.1\.0\].*2025-05-20", line):
            current_block = "0.1.0"
            capture = False
            continue
        if line.startswith("## ") and current_block:
            current_block = None
            capture = False
        if current_block:
            if line.startswith("### "):
                capture = any(k in line for k in ("Added", "Fixed"))
                continue
            if capture and line.startswith("- "):
                sections[current_block].append(line[2:].strip())
    return sections


def extract_task_id(text: str) -> str | None:
    m = re.search(r"\(([^()]+-\d+)\)", text)
    if m:
        return m.group(1)
    lower = text.lower()
    for kw in KEYWORDS:
        if kw in lower:
            return kw
    return None


def create_issues():
    sections = parse_changelog()
    for scope, items in sections.items():
        for line in items:
            tid = extract_task_id(line)
            if tid:
                title = f"{tid}: {line}"
            else:
                title = f"Historical Task: {line}"
            print(f"Creating issue: {title}")
            subprocess.run(
                [
                    "gh",
                    "issue",
                    "create",
                    "--title",
                    title,
                    "--body",
                    "Auto-created from CHANGELOG.md for work completed around 2025-05-20/21.",
                    "--label",
                    "Task-ID,status:done",
                    "--repo",
                    REPO,
                ],
                check=False,
            )


if __name__ == "__main__":
    create_issues()
