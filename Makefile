.PHONY: set-venv
set-venv:
	conda env remove -n pmenv && conda env create -f anaconda-project.yml

.PHONY: run
run:
	conda activate pmenv && python -m src.main

.PHONY: lint
lint:
	conda activate pmenv && pylint src/

.PHONY: test
test:
	conda activate pmenv && python -m pytest test/

.PHONY: test-coverage
test-coverage:
	conda activate pmenv && coverage run -m pytest test/ && coverage report
