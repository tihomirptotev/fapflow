""" Counterparty models. """
from apflow_flask.extensions import db
from .database import reference_col, relationship, AuditMixin, Column, Model


class Counterparty(AuditMixin, Model):
    # __versioned__ = {}
    __tablename__ = 'counterparties'

    name = Column(db.String(length=128), index=True, nullable=False)
    eik_egn = Column(db.String(13), index=True, unique=True, nullable=False)
    notes = relationship('CounterpartyNote',
                         backref='counterparty',
                         lazy='dynamic')
    # accounts = relationship('CounterpartyAccount',
    #                         backref='counterparty',
    #                         lazy='dynamic')
    apdocs = relationship('ApDocument',
                            backref='counterparty',
                            lazy='dynamic')

    # @validates('eik_egn')
    # def validate_eik_egn(self, key, value):
    #     assert (len(value) >= 9) & (len(value) <= 13)
    #     return value


class CounterpartyNote(AuditMixin, Model):
    __tablename__ = 'counterparty_notes'

    counterparty_id = reference_col('counterparties')
    note = Column(db.String(500), index=True)


# class CounterpartyAccount(BaseModel):
#     __tablename__ = 'counterparty_iban'

#     counterparty_id = Column(Integer(), ForeignKey('counterparties.id'))
#     iban = Column(String(22), index=True, unique=True)
#     active = Column(Boolean(name='active_bool'), default=True, nullable=False)
