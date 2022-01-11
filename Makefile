.PHONY: run clean

VENV = venv
PYTHON = $(VENV)/Scripts/python
PIP = $(VENV)/Scripts/pip
DATA_DIR = code/data

run: $(VENV)/Scripts/Activate
	$(PYTHON) code/main.py

$(VENV)/Scripts/Activate: requirements.txt
	python -m venv $(VENV)
	$(PIP) install -r requirements.txt
	
clean:
	rm -rf code/__pycache__
	rm -rf $(VENV)

clean_files:
	rm -f $(DATA_DIR)/*vol.csv

OS_NAME := $(shell uname -s | tr A-Z a-z)
