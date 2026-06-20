#!/usr/bin/env python3
"""Refresh public GitHub metadata for workshop reference repos.

This is a teaching aid: it proves the workshop's external references are real,
current, and distinguishable from optional partner placeholders. It uses direct
repository endpoints rather than broad search so it remains useful with the
lower unauthenticated GitHub API limit.
"""
from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
import json
import os
import sys
import urllib.error
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
REPORTS = ROOT / "reports"
REPORTS.mkdir(parents=True, exist_ok=True)

REPOS = [
    "awslabs/agentcore-samples",
    "awslabs/fullstack-solution-template-for-agentcore",
    "awslabs/agentcore-rl-toolkit",
    "awslabs/bedrock-agentcore-samples-typescript",
    "aws-samples/sample-agentic-chatbot-accelerator",
    "aws-samples/sample-aws-genai-ops-demos",
    "aws-samples/sample-agentic-ai-post-trade-exception-triage",
    "aws-samples/sample-agentcore-deep-research",
    "aws-samples/sample-autonomous-cloud-coding-agents",
    "aws-samples/sample-ai-agent-architectures-agentcore",
    "aws-samples/sample-strands-agents-hands-on-workshop",
    "deepgram/agent",
    "deepgram/browser-agent",
    "deepgram/deepgram-amazon-connect-sample-apps",
    "deepgram/deepgram-audiocodes-bridge",
    "deepgram/voice-agent-python-client",
    "deepgram/voice-agent-nodejs-client",
    "deepgram/voice-agent-function-calling",
    "Saviynt/terraform-provider-saviynt",
    "Saviynt/SaviyntArtifacts",
]


def fetch_repo(full_name: str) -> dict[str, object]:
    url = f"https://api.github.com/repos/{full_name}"
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "aws-agentic-ai-partner-showcase-workshop",
    }
    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=20) as resp:
        data = json.load(resp)
    return {
        "full_name": data["full_name"],
        "html_url": data["html_url"],
        "description": data.get("description") or "",
        "updated_at": data["updated_at"],
        "stargazers_count": data["stargazers_count"],
        "language": data.get("language") or "",
    }


def main() -> int:
    rows: list[dict[str, object]] = []
    errors: list[str] = []
    for repo in REPOS:
        try:
            rows.append(fetch_repo(repo))
        except urllib.error.HTTPError as exc:
            errors.append(f"{repo}: HTTP {exc.code} {exc.reason}")
        except Exception as exc:  # pragma: no cover - network diagnostics only
            errors.append(f"{repo}: {exc}")

    report = REPORTS / "github_reference_status.md"
    lines = [
        "# GitHub reference status",
        "",
        f"Refreshed: {datetime.now(timezone.utc).isoformat()}",
        "",
        "| Repo | Updated | Stars | Language | Description |",
        "|---|---|---:|---|---|",
    ]
    for row in sorted(rows, key=lambda r: str(r["updated_at"]), reverse=True):
        desc = str(row["description"]).replace("|", "\\|")
        lines.append(
            f"| [{row['full_name']}]({row['html_url']}) | {row['updated_at']} | "
            f"{row['stargazers_count']} | {row['language']} | {desc} |"
        )
    if errors:
        lines += ["", "## Refresh errors", ""] + [f"- {err}" for err in errors]
    report.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {report}")
    print(f"Resolved {len(rows)} repos; errors: {len(errors)}")
    return 1 if errors and not rows else 0


if __name__ == "__main__":
    sys.exit(main())
