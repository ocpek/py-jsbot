.PHONY: d-up d-down d-kill
d-up:
	@docker compose up -d

d-down:
	@docker compose down

d-kill:
	@docker compose down --rmi local
