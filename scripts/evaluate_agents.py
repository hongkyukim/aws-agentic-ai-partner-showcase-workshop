#!/usr/bin/env python3
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.partner_agent_stack import IdentityContext, JsonlTraceSink, PartnerShowcaseAgent, SupportTicket, load_json, load_jsonl

RAW = ROOT / "data" / "raw"
REPORTS = ROOT / "reports"
REPORTS.mkdir(parents=True, exist_ok=True)
agent = PartnerShowcaseAgent(JsonlTraceSink(ROOT / "data" / "warehouse" / "eval_traces.jsonl"))
identities = {k: IdentityContext(**v) for k, v in load_json(RAW / "identities.json").items()}
tickets = {row["ticket_id"]: SupportTicket(**row) for row in load_jsonl(RAW / "tickets.jsonl")}
failures = []
lines = ["# Evaluation report", "", "| Case | Expected | Actual | Result |", "|---|---|---|---|"]
for i, case in enumerate(load_jsonl(RAW / "golden_cases.jsonl"), 1):
    decision = agent.handle_ticket(tickets[case["ticket_id"]], identities[case["identity_id"]])
    checks = [decision.intent == case["expected_intent"], decision.allowed == case["expected_allowed"]]
    if "expected_approval" in case:
        checks.append(case["expected_approval"] in decision.approvals_required)
    result = "PASS" if all(checks) else "FAIL"
    expected = f"intent={case['expected_intent']}, allowed={case['expected_allowed']}"
    actual = f"intent={decision.intent}, allowed={decision.allowed}, approvals={decision.approvals_required}"
    lines.append(f"| {i} {case['ticket_id']}/{case['identity_id']} | {expected} | {actual} | {result} |")
    if result == "FAIL":
        failures.append((case, decision))
(REPORTS / "evaluation_report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
if failures:
    print(f"EVALUATION FAILED: {len(failures)} failing cases")
    sys.exit(1)
print(f"EVALUATION PASSED: {i} cases")
print(f"Report: {REPORTS / 'evaluation_report.md'}")
