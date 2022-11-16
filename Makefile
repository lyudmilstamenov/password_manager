.PHONY: set-venv
set-venv:
	conda env remove -n pmenv && conda env create -f environment.yml


.PHONY: run
run:
	conda activate pmenv && python src/console.py