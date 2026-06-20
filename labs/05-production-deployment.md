# Lab 5: Production deployment mapping and GitHub refresh

Start by refreshing the current public GitHub reference status:

```bash
python3 scripts/refresh_github_references.py
```

Open `reports/github_reference_status.md` and identify which repos are most relevant to your team: Python AgentCore samples, full-stack AgentCore templates, TypeScript samples, Deepgram voice-agent examples, or Saviynt identity-governance artifacts.

Map the local components to AWS:

| Local component | AWS / partner production option |
|---|---|
| `PartnerShowcaseAgent` | Amazon Bedrock AgentCore Runtime, Strands Agents, or Fullstack AgentCore Solution Template |
| `JsonlTraceSink` | CloudWatch Logs, X-Ray/OpenTelemetry, S3 evidence bucket |
| `PolicyEngine` | Saviynt entitlement/risk approval checks |
| `VoiceTranscriptTool` | Deepgram live transcription, browser agent, Amazon Connect sample apps, or voice-agent client |
| `ZendeskTicketTool` | Zendesk Support API action group |
| `golden_cases.jsonl` | CI release gate and canary eval suite |

Reference repos to inspect during this lab:

- AgentCore samples: https://github.com/awslabs/agentcore-samples
- Full-stack AgentCore template: https://github.com/awslabs/fullstack-solution-template-for-agentcore
- AgentCore RL toolkit: https://github.com/awslabs/agentcore-rl-toolkit
- TypeScript AgentCore samples: https://github.com/awslabs/bedrock-agentcore-samples-typescript
- Deepgram Agent SDK/widget: https://github.com/deepgram/agent
- Deepgram browser agent: https://github.com/deepgram/browser-agent
- Deepgram + Amazon Connect samples: https://github.com/deepgram/deepgram-amazon-connect-sample-apps
- Saviynt Terraform provider: https://github.com/Saviynt/terraform-provider-saviynt

Deployment checklist:
- least-privilege IAM roles for each tool/action;
- no broad agent role with all SaaS credentials;
- budget alarms and per-environment quotas;
- rollback plan for failed evals;
- current GitHub reference status captured before teaching optional extensions;
- trace ID propagated through every external write;
- human approval for high-risk identity/billing actions.

Team challenge:

1. Choose one refreshed reference repo from `docs/github-references.md`.
2. Write a three-step migration plan from the local class in `src/partner_agent_stack.py` to the chosen repo's runtime/tooling model.
3. Add one golden case that would block production release if the migration regresses identity governance, ticket side effects, or voice-intake behavior.

4Minds extension slot: add the partner's confirmed public repo/API here and implement it as a new tool class with golden cases before live demo. Do not invent an unofficial repo if the partner booth has not provided one.
