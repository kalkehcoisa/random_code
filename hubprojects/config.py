class BaseConfig:
    DEBUG = False
    ACCESS_TOKEN = '1f5e6f5df92733f9c129b127bae19df96a8e3f73'
    DEVELOP = False


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    DEVELOP = True


class ProductionConfig(BaseConfig):
    pass
