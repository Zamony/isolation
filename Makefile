PYTHON=python3

.PHONY: dep run run-unit-tests run-func-tests build clean lint

dep: requirements.txt
	@$(PYTHON) -m venv venv
	. venv/bin/activate; \
	python -m pip install --quiet -r requirements.txt; \
	deactivate;

run: dep
	. venv/bin/activate; \
	python main.py \
	deactivate;

run-unit-tests:
	. venv/bin/activate; \
	python -m unittest tests/test_board.py tests/test_ui.py; \
	deactivate;

run-func-tests:
	. venv/bin/activate; \
	python -m unittest tests/test_ai.py; \
	deactivate;

build: dep clean
	. venv/bin/activate; \
	pyinstaller --name isolation --onefile main.py; \
	deactivate;

wheel: dep clean
	. venv/bin/activate; \
	python setup.py bdist_wheel; \
	pip wheel -r requirements.txt; \
	deactivate;

clean:
	rm -rf dist build __pycache__ isolation.spec *.whl *.egg-info

lint:
	. venv/bin/activate; \
	pylint --disable="C0103,C0301,C0116,C0115,R0914" isolation; \
	deactivate;