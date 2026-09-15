# Task API

Projeto didático de uma API REST de tarefas usando uma stack Python moderna e simples.

## Stack

- Python 3.12+
- FastAPI
- Pydantic
- SQLAlchemy 2
- PostgreSQL 17
- psycopg 3
- uv
- pytest
- Ruff
- GNU Make
- Docker e Docker Compose

## Estrutura

```text
task-api/
├── app/
│   ├── routes/
│   │   └── tasks.py
│   ├── database.py
│   ├── db_models.py
│   ├── init_db.py
│   ├── main.py
│   └── schemas.py
├── tests/
│   ├── conftest.py
│   └── test_tasks.py
├── .dockerignore
├── .env.example
├── .gitignore
├── Dockerfile
├── docker-compose.yml
├── Makefile
├── pyproject.toml
└── uv.lock
```

## Endpoints

| Método | Rota | Ação |
| --- | --- | --- |
| GET | `/` | Confirma que a API está ativa |
| GET | `/health` | Health check simples |
| GET | `/tasks` | Lista tarefas |
| GET | `/tasks/{id}` | Busca uma tarefa |
| POST | `/tasks` | Cria uma tarefa |
| PUT | `/tasks/{id}` | Atualiza uma tarefa |
| DELETE | `/tasks/{id}` | Remove uma tarefa |

A documentação interativa fica em `http://localhost:8001/docs`.

## Desenvolvimento local com uv

Sincronize as dependências:

```bash
make sync
```

Inicie localmente:

```bash
make run
```

Sem `DATABASE_URL`, o modo local usa um arquivo SQLite `task.db`. No Docker Compose, a aplicação usa PostgreSQL.

## Testes e qualidade

```bash
make test
make lint
make format
make check
```

Os testes usam SQLite em memória e não alteram o banco PostgreSQL de desenvolvimento.

## Docker Compose

Opcionalmente copie o arquivo de exemplo:

```bash
cp .env.example .env
```

No Windows, também é possível criar `.env` manualmente. As variáveis possuem valores padrão e o arquivo não é obrigatório para estudo.

Suba API e PostgreSQL:

```bash
make compose-up
```

Veja o status:

```bash
make compose-ps
```

Acompanhe logs:

```bash
make compose-logs
```

Abra o PostgreSQL:

```bash
make db-shell
```

Pare o ambiente:

```bash
make compose-down
```

## Exemplo de tarefa

```json
{
  "title": "Estudar Docker",
  "completed": false
}
```

O título é obrigatório, remove espaços extras nas extremidades e aceita até 200 caracteres.

## Observação sobre o banco

Este projeto é didático e usa `Base.metadata.create_all()` para criar tabelas automaticamente. Isso mantém o estudo focado em FastAPI, SQLAlchemy, PostgreSQL, uv, Make e Docker. Em sistemas com evolução contínua de schema, o passo seguinte seria adotar uma ferramenta de migração.
