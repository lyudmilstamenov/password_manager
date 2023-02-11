.PHONY: set-venv
set-venv:
	conda env remove -n pmenv && conda env create -f anaconda-project.yml

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

.PHONY: test-coverage
test-coverage:
	conda activate pmenv && coverage run -m pytest test/ && coverage report

#.PHONY: set-path
#set-path:
#	conda activate pmenv && anaconda-project set-variable GOOGLE_APPLICATION_CREDENTIALS=$(VAR)
#

.PHONY: set-path
set-path:
	conda activate pmenv && anaconda-project set-variable GOOGLE_APPLICATION_CREDENTIALS=$(VAR) && anaconda-project save
