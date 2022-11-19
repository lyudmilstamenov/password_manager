.PHONY: set-venv
set-venv:
	conda env remove -n pmenv && conda env create -f environment.yml


.PHONY: run
run:
	conda activate pmenv && python -m src.main

.PHONY: run-v
run-v:
	conda activate pmenv && python src/cryptography.py

.PHONY: lint
lint:
	conda activate pmenv && pylint src/

.PHONY: test
test:
	conda activate pmenv && python -m pytest test/