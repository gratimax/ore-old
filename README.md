# Ore

__Travelers, BEWARE!!__ This is essentially _gamma_-stage software.
While bugfixes and PRs and such are welcome, they will most likely get overwritten as I develop this app further.

There is an instance staged to http://ore.dev.gratimax.net with Docker.
Don't get too attached to whatever you put there, because it's most likely going to be reset.

The Sponge package repository.

## Faq

__Q: Why is this on GitHub?__

Simply put, FOSS(Free and Open Source Software) is the best software.
We dislike the closed nature of BukkitDev, and as part of the goal of moving the Minecraft community forward we
have decided to open-source this project and MIT-license from the start.
Anyone can contribute, make an issue or PR, or read the source freely.

This also allows users to run their own Ore repositories if they wish, and we hope to make that easier by
sticking this project in a Docker container.

__Q: Is this project more like BukkitDev or a package manager?__

Yes.

__Q: Elaborate?__

In its current stages Ore looks more like an open-source version of BukkitDev (BOOYAH open source software!).
We plan to eventually create a package manager that consumes an Ore repository that can install plugins.

__Q: So I should tell my doctor to not go ahead with the operation of surgically attaching me to it?__

We're very excited for the possibilities of this project in causing the machine-human singularity but please remember
that it is a zeta-level feature.

__Q: More FAQ soon?__

Yes.

## Development

Written with python 3 and django 1.7.
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
