.PHONY: help install run lint

help:
	@echo "make install - install dependencies"
	@echo "make run ARGS='--count 5 --dry-run' - run the CLI"
	@echo "make lint - basic syntax check"

install:
	pip install -r requirements.txt

run:
	python -m yt_wl_cli.cli $(ARGS)

lint:
	python -m py_compile yt_wl_cli/*.py
