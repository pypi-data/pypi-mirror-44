![POLITICO](https://rawgithub.com/The-Politico/src/master/images/logo/badge.png)

![Datawok](docs/images/datawok.png)

# Datawok

### Quickstart

1. Install the app.

  ```
  $ pip install django-datawok
  ```

2. Add the app to your Django project and configure settings.

  ```python
  INSTALLED_APPS = [
      # ...
      'rest_framework',
      'datawok',
  ]

  #########################
  # datawok settings

  DATAWOK_SECRET_KEY = ""
  DATAWOK_AWS_ACCESS_KEY_ID = ""
  DATAWOK_AWS_SECRET_ACCESS_KEY = ""
  DATAWOK_AWS_REGION = ""
  DATAWOK_AWS_S3_BUCKET = ""
  DATAWOK_S3_UPLOAD_ROOT = ""
  DATAWOK_APP_ROOT = ""
  DATAWOK_QUERY_TIMEOUT = ""
  DATAWOK_QUERY_LIMIT = ""
  DATAWOK_APP_ROOT = ""
  ```

3. Create your Datawok models and add them as string paths in an array in your settings (see [Making Models](docs/models.py) for more).

  ```python
  #########################
  # datawok settings

  DATAWOK_MODELS = ["module_path.model_file.ModelName"]
  ```

4. Make migrations for you new model(s) and run them:
  ```
  $ python manage.py makemigrations
  $ python manage.py migrate
  ```


### Developing

##### Running a development server

Developing python files? Move into example directory and run the development server with pipenv.

  ```
  $ cd example
  $ pipenv run python manage.py runserver
  ```

Developing static assets? Move into the pluggable app's staticapp directory and start the node development server, which will automatically proxy Django's development server.

  ```
  $ cd datawok/staticapp
  $ gulp
  ```

Want to not worry about it? Use the shortcut make command.

  ```
  $ make dev
  ```

##### Setting up a PostgreSQL database

1. Run the make command to setup a fresh database.

  ```
  $ make database
  ```

2. Add a connection URL to the `.env` file.

  ```
  DATABASE_URL="postgres://localhost:5432/datawok"
  ```

3. Run migrations from the example app.

  ```
  $ cd example
  $ pipenv run python manage.py migrate
  ```
