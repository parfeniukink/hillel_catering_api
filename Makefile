.PHONY: run
run:
	python manage.py runserver

.PHONY: worker
worker:
	watchmedo auto-restart --pattern='*.py' --recursive -- celery -A config worker -l INFO

.PHONY: infra
infra:
	docker compose up -d mock_bueno mock_melange mock_uklon database cache broker

.PHONY: test
test:
	python -m pytest tests

.PHONY: prod
prod:
	python -m gunicorn
