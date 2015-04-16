from os import path

ENVIRON = 'development'

PROJECT_ROOT = path.dirname(__file__)

DEBUG = ENVIRON == 'development'
TESTING = DEBUG
SECRET_KEY = '\xce\xa0\xd92x\xf9S!\x0f\x85J\xd4\xda\xd1\xdbQ\x9dH\x0f"\x94%\x15Z'

SITE_NAME = 'Flask S3 Save Example'

SQLALCHEMY_DATABASE_URI = 'sqlite:///%s' % path.join(PROJECT_ROOT, '../dev.db')

USE_S3 = True

S3_BUCKET_NAME = 's3-test-foobar-whizbang'
AWS_ACCESS_KEY_ID = '#'
AWS_SECRET_ACCESS_KEY = '#'
S3_USE_HTTPS = False

SECURITY_PASSWORD_HASH = 'pbkdf2_sha512'
SECURITY_PASSWORD_SALT = 'f80ec7f4-6f71-4417-bba8-e85d30b1c716'
SECURITY_LOGIN_URL = '/login/'
SECURITY_LOGOUT_URL = '/logout/'
