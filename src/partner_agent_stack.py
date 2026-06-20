from __future__ import annotations

from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from pathlib import Path
import json
import re
import uuid
from typing import Any, Iterable


@dataclass(frozen=True)
class IdentityContext:
    user_id: str
    role: str
    department: str
    entitlements: list[str]
    risk_score: int


@dataclass(frozen=True)
class SupportTicket:
    ticket_id: str
    requester_id: str
    channel: str
    transcript: str
    priority: str
    product_area: str


@dataclass(frozen=True)
class AgentDecision:
    trace_id: str
    ticket_id: str
    intent: str
    allowed: bool
    action: str
    partner_pattern: str
    rationale: str
    approvals_required: list[str]
    runbook_steps: list[str]


class JsonlTraceSink:
    def __init__(self, path: Path):
        self.path = path
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def append(self, event: dict[str, Any]) -> None:
        enriched = {"timestamp": datetime.now(timezone.utc).isoformat(), **event}
        with self.path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(enriched, sort_keys=True) + "\n")


class VoiceTranscriptTool:
    """Deepgram-style transcript normalization without requiring live credentials."""

    FILLERS = re.compile(r"\b(um|uh|like|you know)\b", re.IGNORECASE)

    def normalize(self, transcript: str) -> str:
        cleaned = self.FILLERS.sub("", transcript)
        return re.sub(r"\s+", " ", cleaned).strip()


class PolicyEngine:
    """Saviynt-style identity, entitlement, and risk gate."""

    def authorize(self, identity: IdentityContext, intent: str) -> tuple[bool, list[str], str]:
        approvals: list[str] = []
        if intent in {"password_reset", "privileged_access"}:
            if "support:identity-write" not in identity.entitlements:
                return False, ["identity-admin"], "Missing identity-write entitlement."
            if identity.risk_score >= 70:
                approvals.append("security-review")
        if intent == "refund":
            if "support:billing-write" not in identity.entitlements:
                return False, ["billing-manager"], "Missing billing-write entitlement."
            if identity.risk_score >= 70:
                approvals.append("security-review")
        return True, approvals, "Policy checks passed."


class ZendeskTicketTool:
    """Zendesk-style ticket action planner; local only, no external API call."""

    def plan_action(self, ticket: SupportTicket, intent: str) -> tuple[str, list[str]]:
        base = [
            f"Open ticket {ticket.ticket_id} in support workspace.",
            f"Confirm requester {ticket.requester_id} and product area {ticket.product_area}.",
        ]
        if intent == "password_reset":
            return "draft_identity_verification_reply", base + ["Send identity verification workflow.", "Escalate if verification fails."]
        if intent == "refund":
            return "draft_refund_review", base + ["Check billing policy.", "Prepare refund approval note."]
        if intent == "outage":
            return "link_incident_and_update_customer", base + ["Attach active incident.", "Send status-page update."]
        return "draft_support_reply", base + ["Summarize issue.", "Ask one clarifying question if needed."]


class PartnerShowcaseAgent:
    def __init__(self, trace_sink: JsonlTraceSink):
        self.voice = VoiceTranscriptTool()
        self.policy = PolicyEngine()
        self.zendesk = ZendeskTicketTool()
        self.trace_sink = trace_sink

    def classify_intent(self, text: str) -> str:
        lowered = text.lower()
        if any(term in lowered for term in ["password", "login", "locked out", "access"]):
            return "password_reset"
        if any(term in lowered for term in ["refund", "charge", "invoice", "billing"]):
            return "refund"
        if any(term in lowered for term in ["down", "outage", "unavailable", "latency"]):
            return "outage"
        if any(term in lowered for term in ["admin", "privileged", "role"]):
            return "privileged_access"
        return "general_support"

    def handle_ticket(self, ticket: SupportTicket, identity: IdentityContext) -> AgentDecision:
        trace_id = str(uuid.uuid4())
        normalized = self.voice.normalize(ticket.transcript)
        intent = self.classify_intent(normalized)
        allowed, approvals, rationale = self.policy.authorize(identity, intent)
        action, steps = self.zendesk.plan_action(ticket, intent)
        if not allowed:
            action = "request_human_approval"
            steps.append("Stop automation before side effects; queue for authorized reviewer.")
        elif approvals:
            action = f"stage_{action}_pending_approval"
            steps.append("Stage action but require approval before API write.")
        decision = AgentDecision(
            trace_id=trace_id,
            ticket_id=ticket.ticket_id,
            intent=intent,
            allowed=allowed,
            action=action,
            partner_pattern=self._partner_pattern(intent),
            rationale=rationale,
            approvals_required=approvals,
            runbook_steps=steps,
        )
        self.trace_sink.append({"type": "agent_decision", **asdict(decision)})
        return decision

    def _partner_pattern(self, intent: str) -> str:
        if intent in {"password_reset", "privileged_access"}:
            return "Saviynt identity governance + Zendesk ticket workflow"
        if intent == "outage":
            return "AWS production observability + Zendesk proactive support"
        if intent == "refund":
            return "Zendesk workflow with policy-gated business action"
        return "Deepgram voice intake + AWS agent orchestration"


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def write_jsonl(path: Path, rows: Iterable[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, sort_keys=True) + "\n")
