.PHONY: start
start:
	docker compose up -d



.PHONY: run
run:
	python manage.py runserver



.PHONY: worker
worker:
	watchmedo auto-restart --recursive --pattern='*.py' -- celery -A config worker -l INFO



.PHONY: infra
infra:
	docker compose up -d database cache broker mailing

.PHONY: prod
prod:
	docker compose up -d api

.PHONY: bueno
bueno:
	uvicorn tests.providers.bueno:app --reload --port 8002

.PHONY: uklon
uklon:
	uvicorn tests.providers.uklon:app --reload --port 8003



# ==================================================
# CODE QUALITY
# ==================================================
.PHONY: check
check:
	black --check ./
	isort --check ./
	flake8 ./
	mypy ./


.PHONY: quality
quality:
	black ./
	isort ./

.PHONY: test
test:
	python -m pytest tests/ 
