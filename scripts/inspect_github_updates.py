#!/usr/bin/env python3
"""Inspect GitHub remote updates for the workshop repository.

This script is intentionally credential-free by default. It uses the configured
`origin` remote and local git metadata to teach attendees how to review GitHub
updates before merging them into a production workshop branch.
"""
from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
REPORTS = ROOT / "reports"
REPORTS.mkdir(parents=True, exist_ok=True)


def git(*args: str, check: bool = True) -> str:
    result = subprocess.run(
        ["git", *args],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    if check and result.returncode:
        raise RuntimeError(result.stderr.strip() or result.stdout.strip())
    return result.stdout.strip()


def short(ref: str) -> str:
    return git("rev-parse", "--short", ref)


def main() -> int:
    try:
        git("fetch", "origin", "--prune")
    except Exception as exc:
        print(f"Unable to fetch origin: {exc}")
        return 1

    branches = [line.strip() for line in git("branch", "-r", "--format=%(refname:short)").splitlines()]
    origin_branches = [b for b in branches if b.startswith("origin/") and not b.endswith("/HEAD")]
    current = git("branch", "--show-current") or "DETACHED"
    status = git("status", "--short", "--branch")

    lines = [
        "# GitHub remote update report",
        "",
        f"Refreshed: {datetime.now(timezone.utc).isoformat()}",
        f"Current branch: `{current}`",
        "",
        "## Working tree status",
        "",
        "```text",
        status,
        "```",
        "",
        "## Remote branches",
        "",
        "| Branch | Commit | Ahead/behind vs current | Last commit |",
        "|---|---|---|---|",
    ]

    for branch in sorted(origin_branches):
        abbrev = short(branch)
        counts = git("rev-list", "--left-right", "--count", f"HEAD...{branch}")
        ahead, behind = counts.split()
        subject = git("log", "-1", "--pretty=%s", branch)
        lines.append(f"| `{branch}` | `{abbrev}` | current ahead {ahead}, behind {behind} | {subject} |")

    lines += [
        "",
        "## Review workflow for attendees",
        "",
        "1. `git fetch origin --prune`",
        "2. `git log --oneline --decorate --graph --all --max-count=20`",
        "3. `git diff --stat main..origin/<branch>`",
        "4. Open the changed files and decide whether the update improves the workshop.",
        "5. Merge or cherry-pick only after the local workshop path still passes `make test`.",
        "",
        "For this repository, keep local labs authoritative unless a remote branch adds",
        "substantive workshop content. Title-only or placeholder changes should not replace",
        "the verified local-first lab stack.",
    ]

    report = REPORTS / "github_remote_update_report.md"
    report.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {report}")
    print(f"Remote branches inspected: {len(origin_branches)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
