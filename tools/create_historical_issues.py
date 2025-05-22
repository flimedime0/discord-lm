#!/usr/bin/env python
"""
Rebuild PROJECT_STATE.md from GitHub Issues.

Convention:
* Each issue title starts with canonical Task ID, e.g. "dockerize-13: Docker & Compose".
* One of these labels is present: status:todo | status:in-progress | status:done
"""
import re
import subprocess
import pathlib

CHANGELOG_PATH = pathlib.Path("CHANGELOG.md")
REPO_OWNER_SLASH_NAME = "flimedime0/discord-lm-app"  # Ensure this is correct


def parse_changelog_for_tasks(changelog_content: str) -> list[str]:
    tasks = []
    # Regex to find lines under "Added" or "Fixed" in Unreleased or 0.1.0
    # This is a basic example; might need refinement for your exact changelog structure
    pattern = re.compile(r"^\s*-\s*(.+?)(?:\s+([`\[\(][a-zA-Z0-9_-]+[`\]\)]))?$")

    in_relevant_section = False
    for line in changelog_content.splitlines():
        if line.startswith("## [Unreleased]") or line.startswith("## [0.1.0]"):
            in_relevant_section = True
        elif line.startswith("## [") and not (
            line.startswith("## [Unreleased]") or line.startswith("## [0.1.0]")
        ):
            in_relevant_section = False  # Stop if we hit an older version section

        if in_relevant_section and line.strip().startswith("- "):
            match = pattern.match(line.strip())
            if match:
                description = match.group(1).strip()
                task_id_like = match.group(2)[1:-1] if match.group(2) else None
                title_prefix = f"{task_id_like}: " if task_id_like else "Historical Task: "
                tasks.append(f"{title_prefix}{description}")
    return tasks


def create_github_issue(title: str, repo: str):
    body = "Auto-created from CHANGELOG.md for work completed around 2025-05-20/21."
    labels = "Task-ID,status:done"
    command = [
        "gh",
        "issue",
        "create",
        "--title",
        title,
        "--body",
        body,
        "--label",
        labels,
        "--repo",
        repo,
    ]
    try:
        print(f"Attempting to create issue: '{title}'")
        subprocess.run(command, check=True, capture_output=True, text=True)
        print(f"Successfully created issue: '{title}'")
    except subprocess.CalledProcessError as e:
        print(f"Failed to create issue: '{title}'. Error: {e.stderr}")


if __name__ == "__main__":
    if not CHANGELOG_PATH.exists():
        print(f"Error: {CHANGELOG_PATH} not found.")
    else:
        content = CHANGELOG_PATH.read_text()
        discovered_tasks = parse_changelog_for_tasks(content)
        if not discovered_tasks:
            print("No tasks found in changelog to create issues for.")
        else:
            print(
                f"Found {len(discovered_tasks)} tasks. Authenticate with 'gh auth login' if needed."
            )
            for task_title in discovered_tasks:
                create_github_issue(task_title, REPO_OWNER_SLASH_NAME)
            print("Finished attempting to create historical issues.")
