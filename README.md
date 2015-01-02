# Ore

__Travelers, BEWARE!!__ This is essentially _gamma_-stage software.
While bugfixes and PRs and such are welcome, they will most likely get overwritten as I develop this app further.

There is an instance staged to http://ore.dev.gratimax.net with Docker.
Don't get too attached to whatever you put there, because it's most likely going to be reset.

The Sponge package repository.

## Development

Written with python and django.
You should probably use virtualenv.

1.  Create a new virtualenv - my suggestion is to use `virtualenv venv` in the root of the project.
2.  Enter the virtualenv - if you followed my instruction about, use `source venv/bin/activate`.
3.  Install the requirements - `pip install -r requirements/development.txt`
4.  Set up the database - our base development settings expect a database with name `repo`, user `admin` and password `password`.
5.  Perform a migration - `python manage.py migrate`
6.  Start the web server - `python manage.py runserver`

Note that we use Postgres, both in production and development. We can and probably will choose to use Postgres-only features, so beware!

## How to run

Builds are automatically published to [the central Docker registry](https://registry.hub.docker.com/u/gratimax/ore/).

```bash
$ docker run -d --link db:db -e APP_ENV=STAGING -e DB_USER=repo -e DB_PASSWORD=mysecret -e SECRET_KEY=much_secret -p 80:80 gratimax/ore
```
