ai:
	alembic init -t async migrations

ar:
	alembic revision --autogenerate -m "create table"

.PHONY: ai
