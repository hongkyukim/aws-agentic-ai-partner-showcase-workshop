#!/usr/bin/env python3
from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.partner_agent_stack import IdentityContext, JsonlTraceSink, PartnerShowcaseAgent, SupportTicket, load_json, load_jsonl, write_jsonl

RAW = ROOT / "data" / "raw"
WAREHOUSE = ROOT / "data" / "warehouse"
REPORTS = ROOT / "reports"
WAREHOUSE.mkdir(parents=True, exist_ok=True)
REPORTS.mkdir(parents=True, exist_ok=True)

trace_path = WAREHOUSE / "agent_runs.jsonl"
if trace_path.exists():
    trace_path.unlink()
agent = PartnerShowcaseAgent(JsonlTraceSink(trace_path))
identities = {k: IdentityContext(**v) for k, v in load_json(RAW / "identities.json").items()}
tickets = [SupportTicket(**row) for row in load_jsonl(RAW / "tickets.jsonl")]
assignment = {"T-1001": "agent-001", "T-1002": "agent-003", "T-1003": "agent-001", "T-1004": "agent-001"}
rows = []
for ticket in tickets:
    decision = agent.handle_ticket(ticket, identities[assignment[ticket.ticket_id]])
    rows.append(decision.__dict__)
write_jsonl(WAREHOUSE / "decisions.jsonl", rows)

lines = ["# Demo run report", "", "| Ticket | Intent | Allowed | Action | Pattern |", "|---|---|---:|---|---|"]
for row in rows:
    lines.append(f"| {row['ticket_id']} | {row['intent']} | {row['allowed']} | {row['action']} | {row['partner_pattern']} |")
(REPORTS / "demo_run.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
print(f"Processed {len(rows)} tickets")
print(f"Trace: {trace_path}")
print(f"Report: {REPORTS / 'demo_run.md'}")
