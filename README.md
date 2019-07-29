# movies
Django REST Framework application with movie details download from [OMDB API](http://www.omdbapi.com/)

## Requirements
Install PostgreSQL 9.5+, Python 3.7 and Django 2.1

Create postgres account for REST application. Configure database configuration to:
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
python manage.py migrate```

Now you are ready to start django locally:
```python manage.py runserver```

## Run tests
To run unit tests use following command:
```python manage.py test```

## API Specification
API specification is available here: [API](API.md)
