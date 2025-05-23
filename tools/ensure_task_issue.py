#!/usr/bin/env python3
"""Find or create a GitHub issue for a Task ID."""

from __future__ import annotations

import json
import os
import subprocess
import sys


def run_gh_command(args: list[str], input_str: str | None = None) -> str:
    """Helper to run gh commands and return stdout."""
    try:
        process = subprocess.run(
            ["gh"] + args,
            check=True,
            capture_output=True,
            text=True,
            input=input_str,
        )
        return process.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(
            f"Error running gh command {' '.join(args)}: {e.stderr}",
            file=sys.stderr,
        )
        raise


def ensure_task_issue(task_id: str) -> int:
    repo = os.environ["GITHUB_REPOSITORY"]

    # Pass search terms as individual arguments to 'gh search issues'
    # This lets 'gh' handle any necessary quoting or escaping.
    search_terms = [
        task_id,  # The core search term (Task ID itself)
        "in:title",
        f"repo:{repo}",
        "type:issue",
        "label:Task-ID",
    ]
    search_args = [
        "search",
        "issues",
        *search_terms,  # Unpack the terms as separate arguments
        "--json",
        "number",
        "--limit",
        "1",
    ]

    stdout = run_gh_command(search_args)

    try:
        # gh search issues returns a list of issues, even if --limit 1
        # If no issues, it returns an empty list "[]"
        issues_list = json.loads(stdout)
        if issues_list:  # If list is not empty, issue exists
            issue_number = issues_list[0]["number"]
            print(
                f"Found existing issue for '{task_id}': #{issue_number}",
                file=sys.stderr,
            )
            return issue_number
    except json.JSONDecodeError:
        print(
            f"Warning: Could not parse JSON from 'gh search issues': {stdout}",
            file=sys.stderr,
        )
        # Fall through to create if search parsing failed or returned empty
    except IndexError:
        print(
            f"Warning: 'gh search issues' returned an empty list for {task_id}.",
            file=sys.stderr,
        )

    # If no issue found, create it
    print(
        f"No existing issue found for '{task_id}'. Creating new issue.",
        file=sys.stderr,
    )
    create_args = [
        "issue",
        "create",
        "--repo",
        repo,
        "--title",
        task_id,
        "--body",
        f"Auto-created for completed task: {task_id}",
        "--label",
        "Task-ID,status:done",
    ]
    created_issue_url = run_gh_command(create_args)
    try:
        issue_number = int(created_issue_url.split("/")[-1])
        print(
            f"Successfully created issue #{issue_number} with URL: {created_issue_url}",
            file=sys.stderr,
        )
        return issue_number
    except (ValueError, IndexError) as e:
        print(
            f"Error parsing issue number from URL '{created_issue_url}': {e}",
            file=sys.stderr,
        )
        raise SystemExit("Failed to parse issue number from creation URL.")


def main(args: list[str]) -> None:
    if not args:
        print("Usage: ensure_task_issue.py TASK_ID", file=sys.stderr)
        raise SystemExit(1)
    num = ensure_task_issue(args[0])
    print(num)


if __name__ == "__main__":
    main(sys.argv[1:])
