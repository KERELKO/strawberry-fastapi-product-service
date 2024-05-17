EXEC = docker exec -it
APP = app


.PHONY: python
python:
	${EXEC} ${APP} python


.PHONY: psql
psql:
	${EXEC} postgres psql -U postgres -d postgres
