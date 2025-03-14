import logging.config

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": True,
    "formatters": {
        "default": {
            "format": "%(message)s"
        }
    },
    "handlers": {

        "console": {
            "class": "logging.StreamHandler",
            "formatter": "default",
            "level": "ERROR"
        },

        "access": {
            "class": "logging.StreamHandler",
            "formatter": "default",
            "level": "INFO"
        }
    },
    "loggers": {

        "uvicorn.access": {
            "handlers": ["access"],
            "level": "INFO",
            "propagate": False
        },

        "uvicorn.error": {"handlers": ["console"], "level": "ERROR"},
        "uvicorn": {"handlers": ["console"], "level": "ERROR"},
        "fastapi": {"handlers": ["console"], "level": "ERROR"},

        "sqlalchemy": {"handlers": ["console"], "level": "ERROR"},
        "sqlalchemy.engine": {"handlers": ["console"], "level": "ERROR"},
        "sqlalchemy.pool": {"handlers": ["console"], "level": "ERROR"},
        "sqlalchemy.dialects": {"handlers": ["console"], "level": "ERROR"},
        "sqlalchemy.orm": {"handlers": ["console"], "level": "ERROR"},
    },

    "root": {
        "handlers": ["console"],
        "level": "ERROR"
    }
}
