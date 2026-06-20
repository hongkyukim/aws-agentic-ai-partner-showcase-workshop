# Lab 6: Review and integrate the latest GitHub update

Goal: teach attendees how to safely consume a new GitHub branch or remote update without losing the production-ready workshop artifacts.

This lab mirrors a common real-world situation: a repository already has a working local stack, while GitHub receives a branch or web edit from another collaborator or automation tool.

## 1. Inspect remote state

```bash
git fetch origin --prune
git status --short --branch
git log --oneline --decorate --graph --all --max-count=20
python3 scripts/inspect_github_updates.py
```

Read `reports/github_remote_update_report.md`.

## 2. Compare the update before merging

```bash
git diff --stat main..origin/copilot/aws-agentic-ai-partner-showcase
git show --stat --oneline origin/copilot/aws-agentic-ai-partner-showcase
```

Decision rule:

- Merge or cherry-pick changes that add runnable labs, tests, docs, security controls, or validated integrations.
- Do not replace the verified local-first workshop with a title-only or placeholder update.
- Never force-push over a teammate's branch unless the repo owner explicitly asks for history rewrite.

## 3. Validate after every integration

```bash
make test
```

The workshop is not production-ready unless the local path still generates data, runs quality checks, executes the demo, runs evals, and passes unit tests.

## 4. Push safely

Prefer a tokenless remote URL in git config:

```bash
git remote -v
```

If a temporary token is required in a disposable environment, use it only for the push and restore the tokenless URL immediately after. Rotate any personal access token pasted into a terminal or chat transcript.

## 5. Discussion prompt

Ask each team:

1. Which GitHub update did you accept or reject?
2. What evidence showed it was safe?
3. Which tests or evals would you add before allowing a production agent deployment?
