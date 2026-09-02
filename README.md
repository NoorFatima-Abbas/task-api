# Task API

A simple CRUD API for managing a to-do list, built with Python and FastAPI as part of a backend engineering assignment. Task data is stored in a PostgreSQL database running in Docker, and the whole stack (app + database) starts with a single command.

## Tech Stack
- Python 3.11
- FastAPI
- Uvicorn (ASGI server)
- PostgreSQL 16 (containerized)
- Docker & Docker Compose

## Setup & Run

Clone the repo:

```bash
git clone https://github.com/NoorFatima-Abbas/task-api.git
cd task-api
```

Copy the example environment file and start the stack:

```bash
cp .env.example .env
docker compose up
```

That's it — one command brings up both the API and its database. On first run, the `tasks` table is created automatically and seeded with 3 example tasks.

Visit `http://localhost:8000` in your browser, or the interactive API docs at `http://localhost:8000/docs`.

### Environment variables

See `.env.example` for the required variable:

| Variable       | Purpose                                  |
|----------------|-------------------------------------------|
| `DATABASE_URL` | PostgreSQL connection string for the app  |

No secrets are hardcoded — `.env` is git-ignored, and `.env.example` documents the expected keys with placeholder values.

## Endpoints

| Method | Path             | Description                          | Success | Errors        |
|--------|------------------|---------------------------------------|---------|---------------|
| GET    | `/`              | API info (name, version, endpoints)   | 200     | —             |
| GET    | `/health`        | Health check                          | 200     | —             |
| GET    | `/tasks`         | List all tasks                        | 200     | —             |
| GET    | `/tasks/{id}`    | Get a single task by ID               | 200     | 404           |
| POST   | `/tasks`         | Create a new task                     | 201     | 400           |
| PUT    | `/tasks/{id}`    | Update a task's title and/or status   | 200     | 400, 404      |
| DELETE | `/tasks/{id}`    | Delete a task                         | 204     | 404           |

## Example: curl
curl.exe -i http://localhost:8000/tasks/99

HTTP/1.1 404 Not Found
date: Tue, 01 Sep 2026 16:27:01 GMT
server: uvicorn
content-length: 29
content-type: application/json

{"error":"Task 99 not found"}


## Database

Task data lives in PostgreSQL, running as its own container (`postgres:16` image), not as a file on disk. Docker Compose starts both the app and the database together, connected on an internal network — the app reaches the database by its service name (`db`), not `localhost`.

Data persists in a named Docker volume (`taskdata`), so it survives `docker compose down` and `up` cycles. The `tasks` table is created automatically if missing, and seeded with 3 example tasks only when the table is empty — restarting the stack never duplicates or wipes existing data.

**Screenshot of seeded data in Postgres:**
![Postgres tasks table]("D:\INTERNSHP_TASKS\task-api\screenshots\db_screenshot.png")

## Notes

Postgres makes all changes — creates, updates, deletes — permanent across restarts, the same guarantee SQLite gave in earlier assignments, but now backed by a real database server instead of a single file. The routes and their behavior are unchanged from the SQLite version; only the storage engine underneath was swapped.

---

## Stage 4 (A2) — Exploring SQLite by hand

Query: `SELECT * FROM tasks WHERE done = 1;`
Result: returned zero rows before any task was marked complete, confirming the query correctly filters on the `done` column.

## Stage 5 (A2) — Publish & Document

Covered above: why SQLite (Database section, prior version), run command (Setup & Run), screenshot, Stage 4 query above.

## Stage 6 (A2) — AI vs Me

**Prompt used:** (pasted my real in-memory `main.py` + migration requirements: SQLite schema, create-if-missing, seed-once, identical endpoint behavior, 400/404 rules, parameterized queries, output isolated to `ai-version/`)

**What the AI did well:**
- Correct 400/404 error shapes and messages, matching mine exactly
- Parameterized queries throughout, no string-glued SQL
- Seed-only-if-empty logic worked correctly across multiple runs

**What it got wrong:**
- Returned `done` as raw `0`/`1` instead of a JSON boolean (`true`/`false`) — a silent behavior change from the original API that my version avoided by wrapping with `bool(row["done"])`.

**What my prompt left it to decide:**
- Added `AUTOINCREMENT` and `NOT NULL`/`DEFAULT` constraints I never specified — harmless, but undocumented decisions.

**Improved prompt (one addition):** "Ensure the `done` field is returned as a JSON boolean (`true`/`false`), not a raw 0/1 integer, in every response."