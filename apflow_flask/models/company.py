""" Company models. """

from sqlalchemy_utils import ChoiceType
from apflow_flask.extensions import db
from .database import reference_col, relationship, AuditMixin, Column, Model


class CompanyUnitType(AuditMixin, Model):
    """ Company unit types. """

    __tablename__ = 'company_unit_types'
    name = Column(db.String(length=128), index=True, unique=True,
                  nullable=False)
    company_units = relationship('CompanyUnit', lazy='dynamic',
                                 backref='unit_type')

    def __repr__(self):
        return self.name


class CompanyUnit(AuditMixin, Model):
    """ Department, Branch or Office in the organization. """

    __tablename__ = 'company_units'
    id = Column(db.Integer, primary_key=True)
    name = Column(db.String(length=128), index=True, unique=True,
                  nullable=False)
    unit_type_id = reference_col('company_unit_types', nullable=False)
    parent_id = reference_col('company_units', nullable=True)
    parent = relationship('CompanyUnit',
                          backref='children',
                          remote_side=[id])
    users = relationship('User',
                         backref='company_unit',
                         lazy='dynamic')

    def __repr__(self):
        return self.name


class CostAccount(AuditMixin, Model):
    """ Accounts used for cost accounting """

    __tablename__ = 'cost_accounts'

    acc_number = Column(db.String(length=10), index=True,
                        unique=True, nullable=False)
    name = Column(db.String(length=128), index=True, nullable=False)
    active = Column(db.Boolean(name='active_bool'),
                    default=True, nullable=False)
