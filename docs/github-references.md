# Current GitHub reference map

This workshop is intentionally local-first, but each lab maps to active public GitHub repos that attendees can inspect after the event. Snapshot refreshed from GitHub repository metadata/search on 2026-06-20.

## AWS / Amazon Bedrock AgentCore

| Repo | Why it matters for this workshop | Refreshed signal |
|---|---|---|
| https://github.com/awslabs/agentcore-samples | Canonical AgentCore examples for moving agents into production runtime, gateway, memory, policy, and evaluation patterns. | Updated 2026-06-19; 3k+ stars in unauthenticated GitHub metadata. |
| https://github.com/awslabs/fullstack-solution-template-for-agentcore | Full-stack production template for AgentCore deployments; useful for the optional deployment lab. | Updated 2026-06-20. |
| https://github.com/awslabs/agentcore-rl-toolkit | Reinforcement-learning extension path for improving tools/policies after golden evals are stable. | Updated 2026-06-20. |
| https://github.com/awslabs/bedrock-agentcore-samples-typescript | TypeScript sample path for teams that want a browser/full-stack implementation. | Updated 2026-06-10. |
| https://github.com/aws-samples/sample-agentic-chatbot-accelerator | Multi-agent chatbot, voice-to-voice AI, RAG, and Agent Factory accelerator on Bedrock AgentCore. | Updated 2026-06-19. |
| https://github.com/aws-samples/sample-aws-genai-ops-demos | Deployable GenAI operations demos; useful for production observability and runbook examples. | Updated 2026-06-20. |
| https://github.com/aws-samples/sample-agentic-ai-post-trade-exception-triage | Governed AgentCore Runtime/Gateway/Policy/Evaluations pattern for regulated workflow triage. | Updated 2026-06-20. |
| https://github.com/aws-samples/sample-agentcore-deep-research | Agentic deep-research application template on AWS. | Updated 2026-06-19. |
| https://github.com/aws-samples/sample-autonomous-cloud-coding-agents | Autonomous coding agents with orchestration, observability, and governance. | Updated 2026-06-19. |
| https://github.com/aws-samples/sample-ai-agent-architectures-agentcore | Step-by-step evolution from simple to production-ready AgentCore architectures. | Existing workshop baseline. |
| https://github.com/aws-samples/sample-strands-agents-hands-on-workshop | Hands-on Strands Agents workshop with tools, hooks, memory, evals, and AgentCore deployment. | Existing workshop baseline. |

## Deepgram

| Repo | Why it matters |
|---|---|
| https://github.com/deepgram/agent | Voice agent SDK, React components, and embeddable widget for the Deepgram Agent API. |
| https://github.com/deepgram/browser-agent | Web component integration with the Voice Agent API. |
| https://github.com/deepgram/deepgram-amazon-connect-sample-apps | Sample voice-agent apps for Deepgram and Amazon Connect integration. |
| https://github.com/deepgram/deepgram-audiocodes-bridge | Bridge SDK for Deepgram Voice Agent API and AudioCodes. |
| https://github.com/deepgram/voice-agent-python-client | Python client for the Voice Agent API; easiest optional Python extension. |
| https://github.com/deepgram/voice-agent-nodejs-client | Node.js client for the Voice Agent API. |
| https://github.com/deepgram/voice-agent-function-calling | Function-calling reference implementation for voice-agent tool use. |

## Zendesk

| Repo / org | Why it matters |
|---|---|
| https://github.com/zendesk | Official Zendesk GitHub organization; use it to discover current SDKs, apps, and tooling. |

Unauthenticated GitHub repository search did not return a clear, current official `zendesk + ai agent` sample repo. Keep Zendesk integration as an API/action-group pattern in this workshop: draft before execute, carry trace IDs into ticket audit history, and require scoped credentials for ticket writes.

## Saviynt

| Repo | Why it matters |
|---|---|
| https://github.com/Saviynt/terraform-provider-saviynt | Infrastructure-as-code path for identity governance configuration. |
| https://github.com/Saviynt/SaviyntArtifacts | Saviynt public artifacts/reference material. |

## 4Minds

No official public 4Minds GitHub organization/repository was confirmed through unauthenticated GitHub search for `4Minds agentic ai aws`. Keep the 4Minds slot as a partner booth exercise: the team should provide the exact repo/API, then attendees implement it as a policy-gated tool with golden cases before demo.

## Refresh command

Run this from the repo root to refresh direct metadata for the known references:

```bash
python3 scripts/refresh_github_references.py
```

The script does not require credentials. If GitHub rate-limits unauthenticated requests, set a temporary `GITHUB_TOKEN` in your shell for a higher API limit; do not commit it.
