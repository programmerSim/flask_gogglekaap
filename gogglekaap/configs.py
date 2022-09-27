class Config(object):
    """Flask Config"""
    SECRET_KEY = 'secretkey'
    SESSION_COOKIE_NAME = 'gogglekaap'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:password@localhost/gogglekaap?charset=utf8'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SWAGGER_UI_DOC_EXPANSION = 'list'
    
class DevelopmentConfig(Config):
    """Flask Config for dev"""
    DEBUG = True
    SEND_FILE_MAX_AGE_DEFAULT = 1 # 디버깅 모드에서 캐시 제거
    # TODO: Front호출시 처리
    WTF_CSRF_ENABLED = False # 디버깅 모드에서 CSRF 미적용
    
class ProductionConfig(DevelopmentConfig):
    pass