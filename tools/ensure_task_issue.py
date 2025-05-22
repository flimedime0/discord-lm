#!/usr/bin/env python3
"""Find or create a GitHub issue for a Task ID."""

from __future__ import annotations

import json
import os
import subprocess
import sys


def gh(*args: str, input: str | None = None) -> str:
    cmd = ["gh", "api"] + list(args)
    return subprocess.check_output(cmd, text=True, input=input)


def ensure_task_issue(task_id: str) -> int:
    repo = os.environ["GITHUB_REPOSITORY"]
    query = f"repo:{repo} in:title {task_id} type:issue"
    data = json.loads(gh("search/issues", "-f", f"q={query}"))
    if data.get("total_count"):
        return data["items"][0]["number"]
    issue = json.loads(
        gh(
            f"repos/{repo}/issues",
            "-X",
            "POST",
            "-F",
            f"title={task_id}",
            "-F",
            "body=Auto-created for completed task",
        )
    )
    return issue["number"]


def main(args: list[str]) -> None:
    if not args:
        print("Usage: ensure_task_issue.py TASK_ID", file=sys.stderr)
        raise SystemExit(1)
    num = ensure_task_issue(args[0])
    print(num)


if __name__ == "__main__":
    main(sys.argv[1:])
