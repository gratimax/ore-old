from repo.urls import url_patterns
import tornado.web
import os.path
from settings.settings import settings  # lol

# The root Repo application
class Repo(tornado.web.Application):
    def __init__(self):
        tornado.web.Application.__init__(self, url_patterns, **settings)