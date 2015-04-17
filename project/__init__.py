from os import path

from flask import Flask
from flask_admin import Admin
from flask_sqlalchemy import SQLAlchemy
import sqlalchemy_defaults
from flask_migrate import Migrate
from flask_security import Security, SQLAlchemyUserDatastore
from flask_bootstrap import Bootstrap
from flask.ext.uploads import configure_uploads, patch_request_class
from flask_thumbnails_s3 import Thumbnail

from library.admin_utils import ProtectedAdminIndexView


app = Flask(__name__,
            template_folder=path.abspath(
                path.join(path.dirname(__file__), '../templates')),
            static_folder=path.abspath(
                path.join(path.dirname(__file__), '../static')))

app.config.from_object('project.settings')

db = SQLAlchemy(app)
db.Column = sqlalchemy_defaults.Column
sqlalchemy_defaults.make_lazy_configured(db.mapper)

migrate = Migrate(app, db, path.join(app.config['PROJECT_ROOT'], 'migrations'))

from accounts.models import Role, User
security = Security(app, SQLAlchemyUserDatastore(db, User, Role))

Bootstrap(app)

thumb = Thumbnail(app)

from foo.uploads import upload_sets

configure_uploads(app, upload_sets)
patch_request_class(app)

admin = Admin(app,
              name='%s Administration' % app.config['SITE_NAME'],
              index_view=ProtectedAdminIndexView(url='/admin'),
              template_mode='bootstrap3')

import accounts.admin
import foo.admin

from foo.views import mod
app.register_blueprint(mod)
