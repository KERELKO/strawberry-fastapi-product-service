# Product Service

## Description
- __Simple product service, built with [Strawberry](https://strawberry.rocks/) and [FastAPI](https://fastapi.tiangolo.com/)__  
- __[Strawberry](https://strawberry.rocks/) is a developer friendly [GraphQL](https://graphql.org/) library for Python, designed for modern development.__  
- __[GraphQL](https://graphql.org/) is a query language for APIs and a runtime for fulfilling queries with existing data. GraphQL provides a complete and understandable description of the data in API, gives clients the power to ask for exactly what they need and nothing more, makes it easier to evolve APIs over time, and enables powerful developer tools.__

## Brief overview

![image](https://github.com/KERELKO/Strawberry-fastapi-product-service/assets/89779202/493f4c2e-25ed-462d-b018-822fd7e03169)

## Technologies
- [FastAPI](https://fastapi.tiangolo.com/)
- [Postgresql](https://www.postgresql.org/)
- [Docker](https://www.docker.com/)
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [Strawberry](https://strawberry.rocks/)
- [Alembic](https://alembic.sqlalchemy.org/en/latest/)
- [GraphQL](https://graphql.org/)

## How To Use
### Requirements
- Docker
- Docker-compose
- Maketools
### Installation
1. Install the project with
```
git clone https://github.com/KERELKO/strawberry-fastapi-product-service
```
2. Move to directory with __Dockerfile__ and create **.env** file based on **.env.example**
```
touch .env
cat .env.example > .env
```
3. In the same directory run
```
docker compose up
```
4. Go to http://localhost:8000/graphql in your browser and make your queries!

![image](https://github.com/KERELKO/Fastapi-Graphql-product-service/assets/89779202/0546bd5c-2e63-4995-a77f-e776faf8ba6f)

## Contributing

If you'd like to contribute to this project, feel free to fork the repository and submit a pull request. Please follow the existing code style and ensure that all tests pass before submitting your changes.

## Project structure
```
.
├── alembic.ini
├── docker-compose.yaml
├── Dockerfile
├── entrypoint.sh
├── LICENSE
├── Makefile
├── poetry.lock
├── pyproject.toml
├── README.md
├── src
│   ├── common
│   │   ├── base
│   │   │   ├── dto.py
│   │   │   ├── graphql
│   │   │   │   ├── __init__.py
│   │   │   │   ├── resolvers.py
│   │   │   │   └── schemas.py
│   │   │   ├── __init__.py
│   │   │   ├── repo.py
│   │   │   └── uow.py
│   │   ├── constants.py
│   │   ├── db
│   │   │   ├── __init__.py
│   │   │   └── sqlalchemy
│   │   │       ├── base.py
│   │   │       ├── config.py
│   │   │       ├── extensions.py
│   │   │       ├── __init__.py
│   │   │       └── models.py
│   │   ├── di.py
│   │   ├── exceptions.py
│   │   ├── graphql
│   │   │   ├── mutations.py
│   │   │   ├── pagination.py
│   │   │   └── query.py
│   │   ├── __init__.py
│   │   ├── logging
│   │   │   ├── formatters.py
│   │   │   ├── handlers.py
│   │   │   ├── __init__.py
│   │   │   └── loggers.py
│   │   ├── middlewares.py
│   │   ├── settings.py
│   │   └── utils
│   │       ├── fields.py
│   │       ├── graphql.py
│   │       ├── __init__.py
│   │       └── parsers.py
│   ├── __init__.py
│   ├── main.py
│   ├── products
│   │   ├── dto.py
│   │   ├── graphql
│   │   │   ├── converters
│   │   │   │   ├── products.py
│   │   │   │   └── reviews.py
│   │   │   ├── __init__.py
│   │   │   ├── resolvers
│   │   │   │   ├── __init__.py
│   │   │   │   ├── products.py
│   │   │   │   └── reviews.py
│   │   │   └── schemas
│   │   │       ├── __init__.py
│   │   │       ├── products
│   │   │       │   ├── __init__.py
│   │   │       │   ├── inputs.py
│   │   │       │   ├── mutations.py
│   │   │       │   └── queries.py
│   │   │       └── reviews
│   │   │           ├── __init__.py
│   │   │           ├── inputs.py
│   │   │           ├── mutations.py
│   │   │           └── queries.py
│   │   ├── repositories
│   │   │   ├── base.py
│   │   │   └── sqlalchemy
│   │   │       ├── products
│   │   │       │   ├── __init__.py
│   │   │       │   ├── repo.py
│   │   │       │   └── uow.py
│   │   │       └── reviews
│   │   │           ├── __init__.py
│   │   │           ├── repo.py
│   │   │           └── uow.py
│   │   └── services
│   │       ├── products.py
│   │       └── reviews.py
│   └── users
│       ├── dto.py
│       ├── graphql
│       │   ├── converter.py
│       │   ├── __init__.py
│       │   ├── resolver.py
│       │   └── schemas
│       │       ├── __init__.py
│       │       ├── inputs.py
│       │       ├── mutations.py
│       │       └── queries.py
│       ├── __init__.py
│       ├── repositories
│       │   ├── base.py
│       │   ├── __init__.py
│       │   └── sqlalchemy
│       │       ├── __init__.py
│       │       ├── repo.py
│       │       └── uow.py
│       └── service.py
└── tests
```

## TODO
- [ ] Tests
- [x] Mutations
- [ ] Logging
- [ ] Pointer-based Pagination
- [x] At least partly solve the N+1 problem
- [ ] Remake folder structure (graphql as separate folder in src/)
