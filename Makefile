.PHONY: d-up d-down d-kill
UID = $(shell id -u)

d-up:
	@UID=${UID} docker compose up -d

d-down:
	@docker compose down

d-kill:
	@docker compose down --rmi local

d-ps:
	@docker compose ps
