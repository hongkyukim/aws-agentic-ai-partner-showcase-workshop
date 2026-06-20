# From Code to Production: Building Production-Ready AI Agents on AWS

Hands-on workshop repo for the AWS Agentic AI Partner Showcase theme featuring AWS, Saviynt, Deepgram, Zendesk, and 4Minds.

The workshop teaches a production agent stack from code to deployment: voice input, identity-aware authorization, support workflow automation, evaluations, observability, and an optional AWS deployment path.

## What attendees build

A local-first support operations agent that:

1. accepts voice/contact-center transcripts (Deepgram pattern),
2. creates and updates customer support tickets (Zendesk pattern),
3. enforces identity, entitlement, and separation-of-duties checks (Saviynt pattern),
4. orchestrates specialist tools behind policy gates (AWS Bedrock AgentCore / Strands Agents pattern),
5. produces traces, evaluations, and release evidence for production readiness,
6. leaves an integration slot for 4Minds partner-specific workflows once the team chooses the confirmed public repo/API.

The default path uses only Python standard library so every attendee can run it without AWS or SaaS credentials. Cloud/vendor labs are optional extensions.

## Public repo references used for the workshop

Official/public GitHub references found during scaffolding:

| Partner | Public GitHub reference | How it is used in this workshop |
|---|---|---|
| AWS Labs | https://github.com/awslabs/agentcore-samples | Optional production deployment and AgentCore concepts |
| AWS Samples | https://github.com/aws-samples/sample-ai-agent-architectures-agentcore | Evolution from simple agents to production-ready architectures |
| AWS Samples | https://github.com/aws-samples/sample-strands-agents-hands-on-workshop | Optional Strands Agents workshop extension |
| AWS Labs | https://github.com/awslabs/amazon-bedrock-agent-samples | Optional Bedrock Agents extension |
| Deepgram | https://github.com/deepgram/voice-agent-python-client | Optional live voice-agent client extension |
| Zendesk | https://github.com/zendesk | Official Zendesk GitHub org for SDK/examples discovery |
| Saviynt | https://github.com/Saviynt/terraform-provider-saviynt | Optional identity-governance/IaC extension |
| Saviynt | https://github.com/Saviynt/SaviyntArtifacts | Optional Saviynt artifact/reference extension |
| 4Minds | TBD by event team | No official 4Minds GitHub org/repo was confirmed from unauthenticated GitHub search; keep the lab integration slot and replace `TBD` when the partner repo is provided. |

## Quick start

```bash
python3 scripts/generate_sample_data.py
python3 scripts/run_quality_checks.py
python3 scripts/run_demo.py
python3 scripts/evaluate_agents.py
```

Expected artifacts:

- `data/raw/*.jsonl|json` sample event fixtures
- `data/warehouse/agent_runs.jsonl` production-style execution traces
- `reports/demo_run.md` stakeholder-readable run summary
- `reports/evaluation_report.md` eval pass/fail report

## Workshop formats

### 90-minute version

1. Lab 0: local setup and architecture walkthrough (10 min)
2. Lab 1: generate sample support/identity/voice data (10 min)
3. Lab 2: run the local agent stack (20 min)
4. Lab 3: add policy and approval gates (20 min)
5. Lab 4: run evaluations and inspect traces (20 min)
6. Lab 5: AWS/vendor extension discussion (10 min)

### Half-day version

Add the optional AWS extension, partner-booth breakout prompts, and team challenge from `labs/05-production-deployment.md`.

## Repository map

```text
src/partner_agent_stack.py        Local agent, policy, tools, tracing, evaluation primitives
scripts/generate_sample_data.py   Deterministic sample data generator
scripts/run_quality_checks.py     Data and artifact validation
scripts/run_demo.py               End-to-end local demo runner
scripts/evaluate_agents.py        Golden-case production-readiness evals
labs/                             Instructor-led lab guides
prompts/                          Prompts for design reviews and booth discussions
.github/workflows/ci.yml          GitHub Actions local-path validation
```

## Optional AWS path

The local agent mirrors an AWS production architecture:

- Agent runtime/orchestration: Amazon Bedrock AgentCore or Strands Agents
- Knowledge/tools: Lambda, API Gateway, DynamoDB/OpenSearch, Bedrock Knowledge Bases
- Voice: Deepgram live transcription feeding an agent event stream
- Ticketing: Zendesk API actions behind least-privilege credentials
- Identity governance: Saviynt approval/entitlement APIs before sensitive actions
- Observability: CloudWatch logs/metrics plus trace IDs emitted by every tool call
- Evaluation: pre-deploy golden tests, canary tests, and rollback gates

See `labs/05-production-deployment.md` for the deployment mapping and risk controls.

## Safety and cost controls

- No real customer data is included.
- Generated fixtures are deterministic and synthetic.
- Generated outputs are ignored by git.
- SaaS/API keys should be stored in local environment variables or a secrets manager, never committed.
- Optional cloud labs should run in a sandbox AWS account with budget alarms.
