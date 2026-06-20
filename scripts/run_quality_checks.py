#!/usr/bin/env python3
from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"
errors: list[str] = []

def read_jsonl(path: Path):
    if not path.exists():
        errors.append(f"missing {path}")
        return []
    rows = []
    for i, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        try:
            rows.append(json.loads(line))
        except json.JSONDecodeError as exc:
            errors.append(f"{path}:{i} invalid json: {exc}")
    return rows

identities_path = RAW / "identities.json"
identities = json.loads(identities_path.read_text(encoding="utf-8")) if identities_path.exists() else {}
if not identities:
    errors.append("missing or empty identities.json")

tickets = read_jsonl(RAW / "tickets.jsonl")
golden = read_jsonl(RAW / "golden_cases.jsonl")
ticket_ids = {t.get("ticket_id") for t in tickets}
for t in tickets:
    for field in ["ticket_id", "requester_id", "channel", "transcript", "priority", "product_area"]:
        if not t.get(field):
            errors.append(f"ticket missing {field}: {t}")
    if t.get("priority") not in {"low", "medium", "high", "critical"}:
        errors.append(f"invalid priority: {t}")
for case in golden:
    if case.get("ticket_id") not in ticket_ids:
        errors.append(f"golden case references unknown ticket: {case}")
    if case.get("identity_id") not in identities:
        errors.append(f"golden case references unknown identity: {case}")
if errors:
    print("QUALITY CHECKS FAILED")
    for err in errors:
        print(f"- {err}")
    sys.exit(1)
print(f"QUALITY CHECKS PASSED: {len(tickets)} tickets, {len(identities)} identities, {len(golden)} golden cases")
