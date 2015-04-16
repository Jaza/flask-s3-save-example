from flask_admin import AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user


class ProtectedAdminIndexView(AdminIndexView):
    def is_accessible(self):
        return current_user.is_authenticated() and current_user.has_admin_privs


class ProtectedModelView(ModelView):
    page_size = 50

    def __init__(self, *args, **kwargs):
        from project import db

        self.form_optional_types = (db.Boolean, db.String)

        super(ProtectedModelView, self).__init__(*args, **kwargs)

    def is_accessible(self):
        return current_user.is_authenticated() and current_user.has_admin_privs
