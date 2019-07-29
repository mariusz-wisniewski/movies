# movies
Django REST Framework application with movie details download from [OMDB API](http://www.omdbapi.com/)

## Requirements
Install PostgreSQL 11.4+, Python 3.7 and Django 2.1

Create postgres account for REST application. Configure your postgres database:
* src/movies/settings.py ([see more](https://docs.djangoproject.com/en/2.1/ref/settings/#databases)) 
* or export it in environment setting DATABASE_URL (see [dj-database-url](https://github.com/jacobian/dj-database-url)). Example:
```DATABASE_URL=postgres://movie:password@localhost:5432/movies```
and add following code to src/movies/setting.py:
```DATABASES = { 'default': dj_database_url.config() }```

In order to use OMDB API you need to request OMDB API-key and store it in environment setting OMDB_API_KEY (if you don't want to store it in env you have to add it before all manage.py and gunicorn commands).
Add OMDB API-key to src/movies/setting.py:
```OMDB_API_KEY = 'abcd1234'```

## Installation
Install all python requirements and run migration:
```pip install -r requirements.txt```
cd movies
python manage.py migrate

Now you are ready to start django locally:

```python manage.py runserver```

## Run tests
To run unit tests use following command:

```python manage.py test```

## API Specification
API specification is available here: [API](API.md)

## Docker

1. Create an empty project directory.
2. Create a new file called Dockerfile in your project directory and add following content:

  ```FROM python:3
  ENV PYTHONUNBUFFERED 1
  RUN mkdir /code
  WORKDIR /code
  COPY requirements.txt /code/
  RUN pip install -r requirements.txt
  COPY . /code/ 
  ```

3. Copy [requirements](requirements.txt) file to project directory.
4. Create a file called docker-compose.yml in your project directory and add following content:

  ```version: '3'

services:
  db:
    image: postgres
    environment:
      - POSTGRES_USER=movie
      - POSTGRES_PASSWORD=password
      - POSTGRES_DB=movies
    volumes:
      - ./data/postgres:/var/lib/postgresql/data
  web:
    build: .
    container_name: omdb_django
    environment:
      - DATABASE_URL=postgres://movie:password@db:5432/movies
    volumes:
      - .:/copy
    command: bash -c "while !</dev/tcp/db/5432; do sleep 60; done; python /code/movie_rest/manage.py migrate && python /code/movie_rest/manage.py runserver 0.0.0.0:8000"
    depends_on:
      - db
    ports:
      - "8000:8000"
  ```
5. Download [movie_rest](movie_rest) project folder with content.
6. Start containers:
  ```docker-compose up```
