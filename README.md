# INT20H 2024
**Try it online:** `https://d20ybysfnublyy.cloudfront.net/` 🚀

### Project info:
urls:
- api: `http://localhost:8080/api`
- apidocs: `http://localhost:8080/docs/`


### First run
- `docker compose up --build backend`
- `docker compose run --rm backend flask --app backend.wsgi:app db upgrade`


### Run Backend
- `docker compose up backend`

# Run Frontned
- `yarn --cwd ./frontend start`

### Migrations
- Init: `docker compose run --rm backend flask --app backend.wsgi:app db init`
- Create revision: `docker compose run --rm backend flask --app backend.wsgi:app db migrate -m "<some message>"`
- Upgrade to latest revision: `docker compose run --rm backend flask --app backend.wsgi:app db upgrade`


### Proper python package installation
- Run shell: `docker compose run --rm shell`
- Install package: `pdm add <package_name>`
