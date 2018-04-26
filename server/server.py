import logging
import tornado.web
import tornado.ioloop
import Config
import hashlib
from Handlers.IDHandler import IDHandler
from Handlers.RangeHandler import RangeHandler
from Handlers.CookiesHandler import CookiesHandler
from Handlers.SetCounterHandler import SetCounterHandler
from Handlers.RangeBlacklistHandler import RangeBlacklistHandler
from Handlers.CreateProfileHandler import CreateProfileHandler


class DatakServerSide(object):
    def __init__(self):
        try:
            logging.basicConfig(filename=Config.LOG_FILE_PATH,
                                level=logging.INFO,
                                format=Config.CONFIG_FORMAT,
                                datefmt=Config.CONFIG_DATEFMT)
            self.io_loop = tornado.ioloop.IOLoop.instance()

            self.web_application = tornado.web.Application([


                (r"/id",                        IDHandler),
            ], gzip=True)

        except Exception as e:
            logging.error('DatakServerSide_ERROR . Msg: %s' % e)

    def run_server(self):
        try:
            self.web_application.listen(8003)
            self.io_loop.start()
        except Exception as e:
            logging.error('run_server_error . Msg: %s' % e)

    def stop_server(self):
        try:
            self.io_loop.stop()
        except Exception as e:
            logging.error('stop_server_error . Msg: %s' % e)


