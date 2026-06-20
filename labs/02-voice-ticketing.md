# Lab 2: Voice intake and support workflow

Deepgram pattern: normalize noisy voice transcripts before intent classification. Zendesk pattern: turn an agent decision into a ticket-safe action plan.

Exercise:
1. Add a noisy transcript to `scripts/generate_sample_data.py`.
2. Run `make demo`.
3. Verify filler words do not change the intended action.

Optional: replace `VoiceTranscriptTool` with Deepgram's `voice-agent-python-client` in a separate branch.
