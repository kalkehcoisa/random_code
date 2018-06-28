import logging
import logging.config

logging_settings = {
    "version": 1,
    "disable_existing_loggers": True,
    "formatters": {
        "simple": {
            "format": ("%(asctime)s [%(levelname)s] "
                       "%(processName)s:%(process)d "
                       "%(module)s:%(funcName)s() "
                       "%(filename)s:%(lineno)d "
                       "= %(message)s"),
            "datefmt": "%a, %d %b %Y %H:%M:%S %z"
        }
    },

    "handlers": {
        "file_handler": {
            "class": "logging.handlers.RotatingFileHandler",
            "level": "INFO",
            "formatter": "simple",
            "filename": "./logs.log",
            "maxBytes": 10485760,
            "backupCount": 10,
            "encoding": "utf8"
        }
    },

    "loggers": {
        "my_custom_logger": {
            "level": "INFO",
            "handlers": ["file_handler"],
            "propagate": "no"
        },
        "huey": {
            "level": "ERROR",
            "handlers": ["file_handler"],
            "propagate": "no"
        },
    },

    "root": {
        "level": "INFO",
        "handlers": ["file_handler"]
    }
}
logging.config.dictConfig(logging_settings)
logger = logging.getLogger('my_custom_logger')
# logging.getLogger("huey").setLevel(logging.WARNING)
