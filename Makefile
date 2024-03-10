ai:
	alembic init -t async migrations

ar:
	alembic revision --autogenerate -m "create table"

au:
	alembic upgrade head

.PHONY: ai ar au
