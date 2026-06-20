# Prompt: production architecture review

You are reviewing an AI agent architecture for production on AWS. Inspect the repository files first, then answer:

1. What are the trust boundaries?
2. Which actions can create external side effects?
3. Where should human approval be mandatory?
4. Which traces prove a decision was safe?
5. What should block deployment in CI?

Return a short list of concrete changes, ordered by risk reduction.
