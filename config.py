import os

class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SECRET_KEY = 'wojiubugaosuni'
    MAIL_SERVER = 'smtp.qq.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')

    ZSD_MAIL_SUBJECT_PREFIX = '[ZSD博客]'
    ZSD_MAIL_SENDER = 'ZSD博客 管理员 <543421410@qq.com>'
    ZSD_ADMIN = os.environ.get('ZSD_ADMIN')

    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
        DEBUG=True
        HOSTNAME = '172.30.200.252'
        DATABASE = 'zsd'
        USERNAME = 'zsd'
        PASSWORD = 'zsd'
        DB_URI = 'mysql+pymysql://{}:{}@{}:3306/{}?charset=utf8mb4'.format(
                 USERNAME, PASSWORD, HOSTNAME, DATABASE)
        SQLALCHEMY_DATABASE_URI = DB_URI

class TestingConfig(Config):
    TESTING = True
    HOSTNAME = '172.30.200.252'
    DATABASE = 'zsd'
    USERNAME = 'zsd'
    PASSWORD = 'zsd'
    DB_URI = 'mysql+pymysql://{}:{}@{}:3306/{}?charset=utf8mb4'.format(USERNAME, PASSWORD, HOSTNAME, DATABASE)
    SQLALCHEMY_DATABASE_URI = DB_URI

class ProductionConfig(Config):
    PROD = True        


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig
}
