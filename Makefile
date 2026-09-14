VENV := .venv
PY   := $(VENV)/bin/python

.PHONY: help venv install install-predict doctor doctor-offline test test-fast import-weights clean

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) \
		| awk 'BEGIN{FS=":.*?## "};{printf "  \033[36m%-16s\033[0m %s\n",$$1,$$2}'

venv: ## create a 3.11+ virtualenv
	uv venv --python 3.11 $(VENV)

install: venv ## renderer + doctor, no torch
	uv pip install --python $(PY) -e '.[dev]'

install-predict: venv ## + tribev2 and torch (large)
	uv pip install --python $(PY) -e '.[predict,dev]'

doctor: ## preflight this machine (needs weights + predict extra)
	$(PY) -m cortex_hit_encode doctor

doctor-offline: ## renderer path + local cache checks, no hub
	$(PY) -m cortex_hit_encode doctor --offline --renderer

test: ## full suite
	$(PY) -m pytest

test-fast: ## skip the tests that rasterise surfaces
	$(PY) -m pytest -m "not slow"

import-weights: ## copy/hardlink from an existing VideoCortex/HF cache
	@echo "Usage: scripts/import-weights.sh --from /path/to/videocortex-or-hf-cache"

clean:
	rm -rf runs .che-cache .videocortex-cache .pytest_cache **/__pycache__ *.egg-info
