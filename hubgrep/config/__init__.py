class Config:
    DEBUG = False
    TESTING = False
    LOGLEVEL = "debug"
    VERSION = "0.0.0"

    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"
    LANGUAGES = {"en": "English", "de": "Deutsch"}

    ENABLE_CACHE = True
    CACHE_TIME = 3600
    REDIS_URL = "redis://redis:6379/0"

    PAGINATION_PER_PAGE_DEFAULT = 10


class ProductionConfig(Config):
    pass


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
    DEBUG = True
