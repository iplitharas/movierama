# Movierama πΏπ½οΈ ποΈ
Movies social sharing platform 

![project](readme-data/project.png)

## Table of contents
1. [Local development](#local-development)
2. [Local docker development](#local-docker-development)
3. [Project folder structure](#project-folder-structure)
4. [Api docs](#api-docs)

### Local development 
**_NOTE:_**  for local development π» the used database is the `sqlite3`

#### Requirements
1. python version: `3.8.6`
2. poetry version: `1.3.1`

#### Setup your local env:
Run the following command:
```bash
make install-local
```
[![asciicast](https://asciinema.org/a/kjzG3hapztEXstV4RsK8udHuh.svg)](https://asciinema.org/a/kjzG3hapztEXstV4RsK8udHuh)
for creating:
1. new `python venv`: `.env`
2. install the dependencies using `poetry`
3. install the `pre-commit` hooks 
4. Create and run the `migrations`
5. create sample fake `users/movies`

Start the webserver π
```bash
source .env/bin/activate && ./manage.py runserver
```

#### To see all the available π commands run.
```bash
make help  
```
#### Run test-cases
```bash
make test 
```

### Local docker development
For local docker π³  development use the following commands:

Install pre-commit hooks
```bash
make install-hooks
```
Create migrations, migrate and create sample data
```bash
make sample-movies-docker
```
Start containers 
```bash
make dev-up
```
Stop containers
```bash
make dev-down
```

### Project folder structure  

```
movierama
    βββ movies         # Django models 
    βββ accounts       # Custom User model, authenticattion 
    βββ api            # Rest API
    βββ config         # Django global settings
    βββ web_app        # Web application
    βββ templates      # HTML templates
    βββ tests          # Pytest test cases
```

## Api docs 

### For interacting with the API you can see all the available endpoints from:

  * swagger-docs : `/swagger/`
  * redoc: `/redoc/`
  * django-rest-framework :`/api/movies/v1/`


### For examples check: [api-docs-examples](api/api-docs.md) 

**_NOTE:_** β οΈ
1. Due to an open-bug to swagger-docs for the `api` it's 
not possible to `upload` a movie cover. If you want to create a `movie`
with a movie-cover create a new one from the `homepage`
2. the `API` endpoints aren't **used** from the templates, instead the
[web-app-endpoints](https://github.com/iplitharas/movierama/blob/main/web_app/urls.py#L13) are
used
