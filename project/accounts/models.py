from __future__ import print_function

from flask_security import UserMixin, RoleMixin
from flask_security.utils import encrypt_password

from project import db


roles_users = db.Table('roles_users',
        db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
        db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))


class Role(RoleMixin, db.Model):
    """Based on Flask-Security quickstart Role"""

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(255), unique=True)
    description = db.Column(db.String(255), default='')

    @classmethod
    def createrole(cls, session, name, description=None):
        """Creates a new role instance."""

        o = cls(
            name=name,
            description=description
        )
        session.add(o)
        return o

    def __repr__(self):
        return u"{0} ({1})".format(self.name, self.description or 'Role')


class User(UserMixin, db.Model):
    """Based on Flask-Security quickstart User"""

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255), default='')
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))

    def set_password(self, session, password):
        """Encrypts a plain-text user password."""

        self.password = encrypt_password(password)
        session.add(self)

    @classmethod
    def createuser(cls, session, email, password, roles=None):
        """Creates a new user instance."""

        o = cls(
            email=email,
            password=encrypt_password(password),
            roles=roles,
        )
        session.add(o)
        return o

    def __repr__(self):
        return self.email

    @property
    def active(self):
        return True

    @property
    def has_admin_privs(self):
        """Determines if this user has admin privileges."""

        return self.active and self.has_role('admin')
