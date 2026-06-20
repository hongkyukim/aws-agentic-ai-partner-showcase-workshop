from pathlib import Path
import tempfile
import unittest

from src.partner_agent_stack import IdentityContext, JsonlTraceSink, PartnerShowcaseAgent, SupportTicket


class PartnerAgentStackTests(unittest.TestCase):
    def test_identity_write_required_for_password_reset(self):
        with tempfile.TemporaryDirectory() as d:
            agent = PartnerShowcaseAgent(JsonlTraceSink(Path(d) / "trace.jsonl"))
            decision = agent.handle_ticket(
                SupportTicket("T-1", "cust", "voice", "I need a password reset", "high", "identity"),
                IdentityContext("agent", "support", "support", ["support:ticket-write"], 10),
            )
            self.assertFalse(decision.allowed)
            self.assertEqual(decision.action, "request_human_approval")

    def test_outage_is_allowed_for_ticket_write_agent(self):
        with tempfile.TemporaryDirectory() as d:
            agent = PartnerShowcaseAgent(JsonlTraceSink(Path(d) / "trace.jsonl"))
            decision = agent.handle_ticket(
                SupportTicket("T-2", "cust", "voice", "API is down", "critical", "platform"),
                IdentityContext("agent", "support", "support", ["support:ticket-write"], 10),
            )
            self.assertTrue(decision.allowed)
            self.assertEqual(decision.intent, "outage")


if __name__ == "__main__":
    unittest.main()
