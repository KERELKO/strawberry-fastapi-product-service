EXEC = docker exec -it
DB = postgres
APP = app


.PHONY: python
python:
	${EXEC} ${APP} python

.PHONY: psql
psql:
	${EXEC} postgres psql -U postgres -d postgres

.PHONY: bash
bash:
	${EXEC} ${APP} bash
