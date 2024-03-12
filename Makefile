ai:
	alembic init -t async migrations

ar:
	alembic revision --autogenerate -m "migration"

au:
	alembic upgrade head

ad:
	alembic downgrade -1

.PHONY: ai ar au
