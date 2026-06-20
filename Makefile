PYTHON ?= python3

.PHONY: setup data check references github-updates demo eval test clean

setup:
	$(PYTHON) --version

data:
	$(PYTHON) scripts/generate_sample_data.py

check: data
	$(PYTHON) scripts/run_quality_checks.py

references:
	$(PYTHON) scripts/refresh_github_references.py

github-updates:
	$(PYTHON) scripts/inspect_github_updates.py

demo: check
	$(PYTHON) scripts/run_demo.py

eval: demo
	$(PYTHON) scripts/evaluate_agents.py

test: eval
	$(PYTHON) -m unittest discover -s tests -v

clean:
	rm -f data/raw/*.jsonl data/raw/*.json data/warehouse/*.jsonl reports/*.md
