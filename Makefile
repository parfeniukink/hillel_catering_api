.PHONY: run
run:
	python manage.py runserver

.PHONY: infra
infra:
	docker compose up -d mock_bueno mock_melange mock_uklon database cache broker
