ai:
	alembic init -t async migrations

ar:
	alembic revision --autogenerate -m "migration"

au:
	alembic upgrade head

ad:
	alembic downgrade -1

server:
	uvicorn src.main:app --reload --host 0.0.0.0 --port 8001

.PHONY: ai ar au server
