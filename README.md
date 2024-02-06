### INT20H 2024


# First run
- `docker compose up --build backend`
- `docker compose run --rm backend flask --app backend db init`
- `docker compose run --rm backend flask --app backend db upgrade`


# Run Backend
- `docker compose up backend`


# Migrations
- Init: `docker compose run --rm backend flask --app backend db init`
- Create revision: `docker compose run --rm backend flask --app backend db migrate -m "<some message>"`
- Upgrade to latest revision: `docker compose run --rm backend flask --app backend db upgrade`
