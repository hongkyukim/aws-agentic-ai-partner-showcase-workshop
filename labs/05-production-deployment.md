# Lab 5: Production deployment mapping on AWS

Map the local components to AWS:

| Local component | AWS / partner production option |
|---|---|
| `PartnerShowcaseAgent` | Amazon Bedrock AgentCore Runtime or Strands Agents |
| `JsonlTraceSink` | CloudWatch Logs, X-Ray/OpenTelemetry, S3 evidence bucket |
| `PolicyEngine` | Saviynt entitlement/risk approval checks |
| `VoiceTranscriptTool` | Deepgram live transcription / voice agent client |
| `ZendeskTicketTool` | Zendesk Support API action group |
| `golden_cases.jsonl` | CI release gate and canary eval suite |

Deployment checklist:
- least-privilege IAM roles for each tool/action;
- no broad agent role with all SaaS credentials;
- budget alarms and per-environment quotas;
- rollback plan for failed evals;
- trace ID propagated through every external write;
- human approval for high-risk identity/billing actions.

4Minds extension slot: add the partner's confirmed public repo/API here and implement it as a new tool class with golden cases before live demo.
