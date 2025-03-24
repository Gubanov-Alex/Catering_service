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
	docker compose up -d database cache broker

.PHONY: bueno
bueno:
	uvicorn tests.providers.bueno:app --reload --port 8002

.PHONY: melange
melange:
	uvicorn tests.providers.melange:app --reload --port 8001

.PHONY: uber
uber:
	uvicorn tests.providers.uber:app --reload --port 8004

.PHONY: uklon
uklon:
	uvicorn tests.providers.uklon:app --reload --port 8003