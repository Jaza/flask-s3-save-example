from flask_admin import form
from flask_login import current_user
import wtforms.validators

from project import admin, db
from project import User
from library.admin_utils import ProtectedModelView


def validate_password_required_if_confirm(form, field):
    """Validates that a password is required if this is a new user."""

    if form.password2_confirm.data and not field.data:
        raise wtforms.validators.ValidationError('Password is required if \'confirm password\' is given')


class UserView(ProtectedModelView):
    column_list = ('email',)
    form_excluded_columns = ('password',)

    form_args = dict(
        email=dict(
            validators=[wtforms.validators.InputRequired()],
        ))

    def scaffold_form(self):
        from project import app

        form_class = super(UserView, self).scaffold_form()
        form_class.password2 = wtforms.PasswordField('New Password', validators=[validate_password_required_if_confirm, wtforms.validators.EqualTo('password2_confirm', message='Passwords must match')])
        form_class.password2_confirm = wtforms.PasswordField('Repeat Password')

        return form_class

    def on_model_change(self, form, model, is_created):
        if len(model.password2):
            model.set_password(db.session, form.password2.data)


admin.add_view(UserView(User, db.session, name='Users'))
