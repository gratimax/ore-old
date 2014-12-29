# Ore

__Travelers, BEWARE!!__ This is essentially _gamma_-stage software.
While bugfixes and PRs and such are welcome, they will most likely get overwritten as I develop this app further.

There is an instance staged to http://ore.dev.gratimax.net with docker.
Don't get too attached to whatever you put there, because it's most likely going to be reset.

The sponge package repository.

## Development

Written with python, tornado, postgresql, momoko, and other stuff too.
You should probably use virtualenv.

Note the environment variables required to start the application:

- `APP_ENV` in https://github.com/gratimax/ore/blob/master/repo/settings/settings.py#L39
- more variables in https://github.com/gratimax/ore/blob/master/repo/settings/settings_production.py#L5-L12
    (some of these, like `DB_PORT_5432_TCP_ADDR`, are assigned by Docker)

## How to run

Builds are automatically published to [docker](https://registry.hub.docker.com/u/gratimax/ore/).

```bash
$ docker run -d --link db:db -e APP_ENV=STAGING -e DB_USER=repo -e DB_PASSWORD=mysecret -e SECRET_KEY=much_secret -p 80:80 gratimax/ore
```
