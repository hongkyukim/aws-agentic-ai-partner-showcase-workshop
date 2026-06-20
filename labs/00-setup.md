# Lab 0: Setup and architecture

Goal: understand the production agent stack and verify the local environment.

```bash
python3 --version
make setup
```

Architecture: Deepgram-style transcript intake -> AWS-style orchestrator -> Saviynt-style policy gate -> Zendesk-style ticket actions -> traces and evals.

# Instructor note

Run commands from the repository root. The default labs use synthetic data and no external credentials. Optional partner integrations should be done only in a sandbox account or demo tenant.
