.PHONY: d-up d-down d-kill d-ps d-restart d-logs dbshell migrate
UID = $(shell id -u)

d-up:
	@UID=${UID} docker compose up -d

d-down:
	@docker compose down

d-kill:
	@docker compose down --rmi local

d-ps:
	@docker compose ps

d-restart: d-kill d-up

d-logs:
	@docker compose logs -f

dbshell:
	@sqlite3 db/sqlite3/todo.db

migrate:
	@sqlite3 db/sqlite3/todo.db < db/sqlite3/migrations.sql
