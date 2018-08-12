# -*- coding: utf-8 -*-
"""User models."""
import datetime as dt

from flask_login import UserMixin

from apflow_flask.models.database import (
    Column,
    Model,
    SurrogatePK,
    db,
    reference_col,
    relationship
)
from apflow_flask.extensions import bcrypt


class Role(SurrogatePK, Model):
    """A role for a user."""

    __tablename__ = 'roles'
    name = Column(db.String(80), unique=True, nullable=False)
    # user_id = reference_col('users', nullable=True)
    # user = relationship('User', backref='roles')

    # def __init__(self, name, **kwargs):
    #     """Create instance."""
    #     db.Model.__init__(self, name=name, **kwargs)

    def __repr__(self):
        """Represent instance as a unique string."""
        return self.name


class User(UserMixin, SurrogatePK, Model):
    """A user of the app."""

    __tablename__ = 'users'
    username = Column(db.String(80), unique=True, nullable=False)
    email = Column(db.String(80), unique=True, nullable=False)
    #: The hashed password
    password = Column(db.String(128), nullable=True)
    created_at = Column(db.DateTime, nullable=False, default=dt.datetime.utcnow)
    first_name = Column(db.String(30), nullable=True)
    last_name = Column(db.String(30), nullable=True)
    active = Column(db.Boolean(), default=False)
    is_admin = Column(db.Boolean(), default=False)
    company_unit_id = reference_col('company_units', nullable=True)
    roles = relationship('Role', secondary='user_roles')

    def __init__(self, username, email, password=None, **kwargs):
        """Create instance."""
        db.Model.__init__(self, username=username, email=email, **kwargs)
        if password:
            self.set_password(password)
        else:
            self.password = None

    def set_password(self, password):
        """Set password."""
        self.password = bcrypt.generate_password_hash(password)

    def check_password(self, value):
        """Check password."""
        return bcrypt.check_password_hash(self.password, value)

    @classmethod
    def find_by_identity(cls, identity):
        user = User.query.filter(
            (User.username == identity) | (User.email == identity)).first()
        return user

    @property
    def full_name(self):
        """Full user name."""
        return '{0} {1}'.format(self.first_name, self.last_name)

    @property
    def roles_list(self):
        return [role.name for role in self.roles]

    def has_role(self, role):
        return role in self.roles_list

    def __repr__(self):
        """Represent instance as a unique string."""
        return '{} - {}'.format(self.username, self.full_name)


class UserRoles(db.Model):
    __tablename__ = 'user_roles'
    id = Column(db.Integer(), primary_key=True)
    user_id = Column(db.Integer(), db.ForeignKey('users.id', ondelete='CASCADE'))
    role_id = Column(db.Integer(), db.ForeignKey('roles.id', ondelete='CASCADE'))
