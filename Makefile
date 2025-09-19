.PHONY: start-extr, build-model

start-extract:
	./.venv/bin/python src/main.py

build-model:
	./build_model.sh