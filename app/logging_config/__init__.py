import logging
import os
from logging.config import dictConfig

import flask
from flask import request, current_app
from sqlalchemy.sql.functions import user

from app.logging_config.log_formatters import RequestFormatter
from app.logging_config.log_formatters import HandlerFormatter
from app.logging_config.log_formatters import CSVFormatter
from app import config

log_con = flask.Blueprint('log_con', __name__)


# @log_con.before_app_request
def before_request_logging():
    current_app.logger.info(user.email)

def CSV_file_upload():
    log=logging.getLogger("myCSVuploads")
    log.info("New CSV uploaded")

@log_con.after_app_request
def after_request_logging(response):
    if request.path == '/favicon.ico':
        return response
    elif request.path.startswith('/static'):
        return response
    elif request.path.startswith('/bootstrap'):
        return response
    return response




@log_con.before_app_first_request
def setup_logs():
    # set the name of the apps log folder to logs
    logdir = config.Config.LOG_DIR
    # make a directory if it doesn't exist
    if not os.path.exists(logdir):
        os.mkdir(logdir)
    logging.config.dictConfig(LOGGING_CONFIG)


LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        },

        'RequestFormatter': {
            '()': 'app.logging_config.log_formatters.RequestFormatter',
            'format': '[%(asctime)s] [%(process)s] %(remote_addr)s requested %(url)s'
                      '%(levelname)s in %(module)s: %(message)s'
        },

        'HandlerFormatter': {
            '()': 'app.logging_config.log_formatters.HandlerFormatter',
            'format': '[%(asctime)s] %(levelname)s METHOD: %(request_method)s FILENAME:%(filename)s FUNCTION NAME:%(funcName)s() LINE:%(lineno)s] %(message)s from %(remote_addr)s'
        },

        'CSVFormatter': {
            '()': 'app.logging_config.log_formatters.CSVFormatter',
            'format': '[%(asctime)s] %(levelname)s METHOD: %(request_method)s FILENAME:%(filename)s FUNCTION NAME:%(funcName)s() LINE:%(lineno)s] %(message)s from %(remote_addr)s'
        },

    },
    'handlers': {
        'default': {
            'level': 'DEBUG',
            'formatter': 'standard',
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stdout',  # Default is stderr
        },
        'file.handler': {
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'HandlerFormatter',
            'filename': os.path.join(config.Config.LOG_DIR, 'handler.log'),
            'maxBytes': 10000000,
            'backupCount': 5,
        },
        'file.handler.myapp': {
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'standard',
            'filename': os.path.join(config.Config.LOG_DIR, 'myapp.log'),
            'maxBytes': 10000000,
            'backupCount': 5,
        },
        # 'file.handler.request': {
        #     'class': 'logging.handlers.RotatingFileHandler',
        #     'formatter': 'standard',
        #     'filename': os.path.join(config.Config.LOG_DIR,'request.log'),
        #     'maxBytes': 10000000,
        #     'backupCount': 5,
        # },
        'file.handler.errors': {
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'standard',
            'filename': os.path.join(config.Config.LOG_DIR, 'errors.log'),
            'maxBytes': 10000000,
            'backupCount': 5,
        },
        'file.handler.sqlalchemy': {
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'standard',
            'filename': os.path.join(config.Config.LOG_DIR, 'sqlalchemy.log'),
            'maxBytes': 10000000,
            'backupCount': 5,
        },
        'file.handler.werkzeug': {
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'standard',
            'filename': os.path.join(config.Config.LOG_DIR, 'werkzeug.log'),
            'maxBytes': 10000000,
            'backupCount': 5,
        },
        'file.handler.requests': {
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'standard',
            'filename': os.path.join(config.Config.LOG_DIR, 'requests.log'),
            'maxBytes': 10000000,
            'backupCount': 5,
        },
        'file.handler.debugs': {
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'standard',
            'filename': os.path.join(config.Config.LOG_DIR, 'debugs.log'),
            'maxBytes': 10000000,
            'backupCount': 5,
        },
        'file.handler.CSVUploads': {
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'CSVFormatter',
            'filename': os.path.join(config.Config.LOG_DIR, 'CSVUploads.log'),
            'maxBytes': 10000000,
            'backupCount': 5,
        },
    },
    'loggers': {
        '': {  # root logger
            'handlers': ['default', 'file.handler'],
            'level': 'DEBUG',
            'propagate': True
        },
        '__main__': {  # if __name__ == '__main__'
            'handlers': ['default', 'file.handler'],
            'level': 'DEBUG',
            'propagate': True
        },
        'werkzeug': {  # if __name__ == '__main__'
            'handlers': ['file.handler.werkzeug'],
            'level': 'DEBUG',
            'propagate': False
        },
        'sqlalchemy.engine': {  # if __name__ == '__main__'
            'handlers': ['file.handler.sqlalchemy'],
            'level': 'INFO',
            'propagate': False
        },
        'myApp': {  # if __name__ == '__main__'
            'handlers': ['file.handler.myapp'],
            'level': 'DEBUG',
            'propagate': False
        },
        'myerrors': {  # if __name__ == '__main__'
            'handlers': ['file.handler.errors'],
            'level': 'DEBUG',
            'propagate': False
        },
        'myrequests': {  # if __name__ == '__main__'
            'handlers': ['file.handler.requests'],
            'level': 'DEBUG',
            'propagate': False
        },
        'mydebugs': {  # if __name__ == '__main__'
            'handlers': ['file.handler.debugs'],
            'level': 'DEBUG',
            'propagate': False
        },
        'myCSVuploads': {  # if __name__ == '__main__'
            'handlers': ['file.handler.CSVUploads'],
            'level': 'INFO',
            'propagate': False
        },
    }
}
