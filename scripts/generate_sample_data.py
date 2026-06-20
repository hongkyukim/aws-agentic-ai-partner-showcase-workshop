#!/usr/bin/env python3
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"
RAW.mkdir(parents=True, exist_ok=True)

identities = {
    "agent-001": {"user_id": "agent-001", "role": "support_agent", "department": "support", "entitlements": ["support:ticket-write"], "risk_score": 20},
    "agent-002": {"user_id": "agent-002", "role": "identity_specialist", "department": "security", "entitlements": ["support:ticket-write", "support:identity-write"], "risk_score": 35},
    "agent-003": {"user_id": "agent-003", "role": "billing_specialist", "department": "finance", "entitlements": ["support:ticket-write", "support:billing-write"], "risk_score": 82},
}

tickets = [
    {"ticket_id": "T-1001", "requester_id": "cust-101", "channel": "voice", "transcript": "um I am locked out and need a password reset before payroll closes", "priority": "high", "product_area": "identity"},
    {"ticket_id": "T-1002", "requester_id": "cust-202", "channel": "chat", "transcript": "Our invoice has a duplicate charge and we need a refund", "priority": "medium", "product_area": "billing"},
    {"ticket_id": "T-1003", "requester_id": "cust-303", "channel": "voice", "transcript": "The API is down and customers see high latency", "priority": "critical", "product_area": "platform"},
    {"ticket_id": "T-1004", "requester_id": "cust-404", "channel": "email", "transcript": "Can you explain how to invite a teammate", "priority": "low", "product_area": "workspace"},
]

golden_cases = [
    {"ticket_id": "T-1001", "identity_id": "agent-001", "expected_intent": "password_reset", "expected_allowed": False},
    {"ticket_id": "T-1001", "identity_id": "agent-002", "expected_intent": "password_reset", "expected_allowed": True},
    {"ticket_id": "T-1002", "identity_id": "agent-003", "expected_intent": "refund", "expected_allowed": True, "expected_approval": "security-review"},
    {"ticket_id": "T-1003", "identity_id": "agent-001", "expected_intent": "outage", "expected_allowed": True},
]

(RAW / "identities.json").write_text(json.dumps(identities, indent=2, sort_keys=True), encoding="utf-8")
for name, rows in [("tickets.jsonl", tickets), ("golden_cases.jsonl", golden_cases)]:
    with (RAW / name).open("w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, sort_keys=True) + "\n")
print(f"Generated {len(tickets)} tickets, {len(identities)} identities, {len(golden_cases)} golden cases under {RAW}")
