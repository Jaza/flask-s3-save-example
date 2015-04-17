from os import path

ENVIRON = 'development'

PROJECT_ROOT = path.dirname(__file__)

DEBUG = ENVIRON == 'development'
TESTING = DEBUG
SECRET_KEY = '\xce\xa0\xd92x\xf9S!\x0f\x85J\xd4\xda\xd1\xdbQ\x9dH\x0f"\x94%\x15Z'

SITE_NAME = 'Flask S3 Save Example'

SQLALCHEMY_DATABASE_URI = 'sqlite:///%s' % path.join(PROJECT_ROOT, '../dev.db')

UPLOADS_RELATIVE_PATH = 'uploads/'
UPLOADS_FOLDER = path.abspath(path.join(PROJECT_ROOT, '../static/%s' % UPLOADS_RELATIVE_PATH))

MEDIA_FOLDER = path.abspath(path.join(PROJECT_ROOT, '../static/%s' % UPLOADS_RELATIVE_PATH.replace('/', '')))
MEDIA_URL = '/static/%s' % UPLOADS_RELATIVE_PATH

MEDIA_THUMBNAIL_FOLDER = path.abspath(path.join(PROJECT_ROOT, '../static/cache/thumbnails'))
MEDIA_THUMBNAIL_URL = 'cache/thumbnails/'

USE_S3 = True

S3_BUCKET_NAME = 's3-test-foobar-whizbang'
AWS_ACCESS_KEY_ID = '#'
AWS_SECRET_ACCESS_KEY = '#'
S3_USE_HTTPS = False

SECURITY_PASSWORD_HASH = 'pbkdf2_sha512'
SECURITY_PASSWORD_SALT = 'f80ec7f4-6f71-4417-bba8-e85d30b1c716'
SECURITY_LOGIN_URL = '/login/'
SECURITY_LOGOUT_URL = '/logout/'

THINGY_IMAGE_RELATIVE_PATH = 'thingy_image/'

THUMBNAIL_S3_STORAGE_TYPE = USE_S3 and 's3' or None
THUMBNAIL_S3_BUCKET_NAME = S3_BUCKET_NAME
THUMBNAIL_S3_ACCESS_KEY_ID = AWS_ACCESS_KEY_ID
THUMBNAIL_S3_ACCESS_KEY_SECRET = AWS_SECRET_ACCESS_KEY
THUMBNAIL_S3_USE_HTTPS = S3_USE_HTTPS
THUMBNAIL_S3_STATIC_ROOT_PARENT = path.abspath(path.join(PROJECT_ROOT, '..'))
