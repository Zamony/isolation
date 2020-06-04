PYTHON=python3

.PHONY: dep run run-unit-tests run-func-tests build clean lint doc

dep: requirements.txt
	@$(PYTHON) -m venv venv
	. venv/bin/activate; \
	python -m pip install --quiet -r requirements.txt; \
	deactivate;

run: dep
	. venv/bin/activate; \
	python main.py; \
	deactivate;

run-unit-tests:
	. venv/bin/activate; \
	python -m unittest tests/test_board.py tests/test_ui.py tests/test_player.py; \
	deactivate;

run-func-tests:
	. venv/bin/activate; \
	python -m unittest tests/test_ai.py tests/test_game.py; \
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
	rm -rf dist build __pycache__ isolation.spec *.whl *.egg-info doc

lint:
	. venv/bin/activate; \
	pylint --disable="C0103,C0301,C0116,C0115,R0914" isolation; \
	deactivate;

doc:
	mkdir -p doc
	. venv/bin/activate; \
	python -m pydoc -w `find isolation -name '*.py' | sed 's+/+.+g' | sed 's+.py++g'`; \
	python -m pydoc -w isolation; \
	deactivate;
	cp isolation.html index.html
	mv *.html doc