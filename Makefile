install:
	poetry install

debug-mode:
	poetry run flask --app page_analyzer:app --debug run --port 8000

dev:
	poetry run flask --app page_analyzer:app run

PORT ?= 8000
start:
	poetry run gunicorn -w 5 -b 0.0.0.0:$(PORT) page_analyzer:app

build:
	./build.sh

lint:
	poetry run flake8 page_analyzer

test:
	poetry run pytest
