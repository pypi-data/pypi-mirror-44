Python Logging Loggly Handler
-----------------------------

A simple Python logging Loggly handler that can be used to send to a https endpoint. Borrowed the extra fields concept from the graypy logging library.

## History
This repository if originally forked from (https://github.com/varshneyjayant/loggly-python-handler)

## Installation
Download the repository using pip

    sudo pip install loggly-python-handler

## Use in python
### Configuration

Create a Configuration file python.conf and add RocketChatHandler to Configuration File.

    [handlers]
    keys=RocketChatHandler

    [handler_RocketChatHandler]
    class=oxomo.handlers.RocketChatHandler
    formatter=jsonFormat
    args=('ROCKETCHAT_WEBHOOK_URL','POST')

    [formatters]
    keys=jsonFormat

    [loggers]
    keys=root

    [logger_root]
    handlers=RocketChatHandler
    level=ERROR

    [formatter_jsonFormat]
    format={ "loggerName":"%(name)s", "asciTime":"%(asctime)s", "fileName":"%(filename)s", "logRecordCreationTime":"%(created)f", "functionName":"%(funcName)s", "levelNo":"%(levelno)s", "lineNo":"%(lineno)d", "time":"%(msecs)d", "levelName":"%(levelname)s", "message":"%(message)s"}
    datefmt=

### Use Configuration in python file

    import logging
    import logging.config
    import oxomo.handlers

    logging.config.fileConfig('python.conf')
    logger = logging.getLogger('myLogger')

    logger.error('Test Error Log')

## optionally log uncaught exceptions as errors

    def sysexcept_handler(type, value, tb):
        logger.error("Uncaught exception: {0}".format(str(value)))
        sys.__excepthook__(type, value, tb)
    sys.excepthook = sysexcept_handler

## Use in Django

### settings.py

    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'verbose': {
                'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
            },
            'simple': {
                'format': '%(levelname)s %(message)s'
            },
            'json': {
                'format': '{ "loggerName":"%(name)s", "asciTime":"%(asctime)s", "fileName":"%(filename)s", "logRecordCreationTime":"%(created)f", "functionName":"%(funcName)s", "levelNo":"%(levelno)s", "lineNo":"%(lineno)d", "time":"%(msecs)d", "levelName":"%(levelname)s", "message":"%(message)s"}',
            },
        },
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'level': 'DEBUG',
                'formatter': 'verbose',
            },
            'oxomo': {
                'class': 'oxomo.handlers.RocketChatHandler',
                'level': 'INFO',
                'formatter': 'json',
                'url': 'ROCKETCHAT_WEBHOOK_URL',
            },
        },
        'loggers': {
            'django': {
                'handlers': ['console', ],
                'level': os.getenv('DJANGO_LOG_LEVEL', 'INFO'),
            },
            'your_app_name': {
                'handlers': ['console', 'oxomo'],
                'level': 'INFO',
            },
        },
    }

### views.py

    import logging

    logger = logging.getLogger(__name__)

    def logging_example(request):
        """logging example
        """
        logger.debug('this is DEBUG message.')
        logger.info('this is INFO message.')
        logger.warning('this is WARNING message.')
        logger.error('this is ERROR message.')
        logger.critical('this is CRITICAL message.')

        return Response({}, status=status.HTTP_200_OK)
