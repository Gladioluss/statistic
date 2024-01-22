#!/usr/bin/make

include dev.env


help:
	@echo "make"
	@echo "    run-dev"
	@echo "        Run development docker compose."
	@echo "    stop-dev"
	@echo "        Stop development docker compose."
	@echo "    run-app"
	@echo "        Run fastapi app."
	@echo "    ruff"
	@echo "        Lint code with ruff."
	@echo "    ruff-fix"
	@echo "        Lint code with ruff and try to fix."
	@echo "    revision"
	@echo "        Create new alembic migration version."
	@echo "    upgrade"
	@echo "        Add new database migration using alembic."
	@echo "    downgrade"
	@echo "        Remove database migration using alembic."


run-dev:
	docker compose -f docker-compose.local.yaml up -d

stop-dev:
	docker compose -f docker-compose.local.yaml down

run-app:
	uvicorn app.main:app --reload --port $(PORT)

ruff:
	ruff check app

ruff-fix:
	ruff check app --fix

revision:
	alembic revision --autogenerate

upgrade:
	alembic upgrade head

downgrade:
	alembic downgrade base