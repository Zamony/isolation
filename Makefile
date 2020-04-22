PYTHON=python3

.PHONY: dep run build clean

dep: requirements.txt
	@$(PYTHON) -m venv venv
	. venv/bin/activate; \
	python -m pip install --quiet -r requirements.txt; \
	deactivate;

run: dep
	. venv/bin/activate; \
	python main.py \
	deactivate;

build: dep clean
	. venv/bin/activate; \
	pyinstaller --name isolation --onefile main.py; \
	deactivate;

clean:
	rm -rf dist build __pycache__ isolation.spec