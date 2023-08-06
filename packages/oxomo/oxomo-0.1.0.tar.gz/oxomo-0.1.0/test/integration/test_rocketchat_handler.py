import logging
import logging.config
import os

_LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format':
            '%(levelname)s %(asctime)s %(module)s %(process)d\
             %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
        'json': {
            'format':
            '{ "loggerName":"%(name)s", "asciTime":"%(asctime)s", "fileName":\
            "%(filename)s", "logRecordCreationTime":"%(created)f",\
            "functionName":"%(funcName)s", "levelNo":"%(levelno)s",\
            "lineNo":"%(lineno)d", "time":"%(msecs)d", "levelName":\
            "%(levelname)s", "message":"%(message)s"}',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'DEBUG',
            'formatter': 'verbose',
        },
        'rocketchat': {
            'class': 'oxomo.handlers.RocketChatHandler',
            'level': 'ERROR',
            'formatter': 'json',
            'url': os.environ['ROCKETCHAT_WEBHOOK']
        },
    },
    'loggers': {
        '': {
            'level': 'DEBUG',
            'handlers': ['rocketchat']
        }
    },
}


class TestRocketChat:
    def setup_class(self):
        pass

    def test_logging_to_rocketchat(self):
        logging.config.dictConfig(_LOGGING)
        logger = logging.getLogger(__name__)

        logger.error('this is ERROR message.')