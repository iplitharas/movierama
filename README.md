# Movierama 🍿📽️ 🎞️
Movies social sharing platform 

## Table of contents
1. [Local development](#local-development)
2. [Local docker development](#local-docker-development)

### Local development 
**_NOTE:_**  for local development 💻 the used database is the `sqlite3`

#### Requirements
1. python version: `3.8.6`
2. poetry version: `1.3.1`

#### Setup your local env:
Run the following command:
```bash
make install-local
```
for creating:
1. new `python venv`: `.env`
2. install the dependencies using `poetry`
3. install the `pre-commit` hooks 
4. Create and run the `migrations`
5. create sample fake `users/movies`

Start the webserver
```bash
source .env/bin/activate && ./manage.py runserver
```

#### To see all the available commands run.
```bash
make help 
```
#### Run test-cases
```bash
make test 
```

### Local docker development
For local docker 🐳  development use the following commands:

Install pre-commit hooks
```bash
make install-hooks
```
Start containers 
```bash
make dev-up
```
Stop containers
```bash
make dev-down
```