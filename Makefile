.DEFAULT_GOAL := help

.PHONY: help sync run test lint format check compose-up compose-down compose-logs compose-ps db-shell init-db

help:
	@echo "Task API - comandos disponíveis:"
	@echo "  make sync         - Sincroniza dependências com uv"
	@echo "  make run          - Inicia a API localmente na porta 8001"
	@echo "  make test         - Executa os testes"
	@echo "  make lint         - Verifica qualidade do código"
	@echo "  make format       - Corrige e formata o código"
	@echo "  make check        - Executa lint e testes"
	@echo "  make compose-up   - Sobe API + PostgreSQL"
	@echo "  make compose-down - Para os serviços"
	@echo "  make compose-logs - Acompanha os logs"
	@echo "  make compose-ps   - Mostra o status dos serviços"
	@echo "  make db-shell     - Abre o psql do PostgreSQL"
	@echo "  make init-db      - Cria tabelas manualmente"

sync:
	uv sync

run:
	uv run uvicorn app.main:app --reload --port 8001

test:
	uv run python -m pytest

lint:
	uv run ruff check app tests

format:
	uv run ruff check app tests --fix
	uv run ruff format app tests

check: lint test

compose-up:
	docker compose up --build -d

compose-down:
	docker compose down

compose-logs:
	docker compose logs -f

compose-ps:
	docker compose ps

db-shell:
	docker compose exec db psql -U $${POSTGRES_USER:-taskuser} -d $${POSTGRES_DB:-taskdb}

init-db:
	docker compose exec api uv run python -m app.init_db
