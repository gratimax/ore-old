#!/usr/bin/env python
from repo.app import Repo

import tornado.httpserver
import tornado.ioloop
from tornado.options import options
import tornado.web
import logging


def main():
    app = Repo()
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    logging.log(logging.INFO, 'Starting on port %i' % (options.port))
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    main()