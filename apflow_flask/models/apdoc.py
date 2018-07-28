from .database import db, AuditMixin, Model, reference_col, Column, relationship

class DocType(AuditMixin, Model):

    __table_name__ = 'doc_types'

    type_name = Column(db.String(length=30))


class ApDocument(AuditMixin, Model):
    """ Account payable document """

    __tablename__ = 'ap_documents'

    counterparty_id = reference_col('counterparties')
    init_unit_id = reference_col('company_units')
    doc_number = Column(db.String(length=20))
    doc_date = Column(db.Date, nullable=False)
    doc_sum = Column(db.Numeric)
    doc_info = Column(db.UnicodeText, nullable=False)
    doc_info_additional = Column(db.UnicodeText, nullable=True)
    doc_type = Column(db.String(length=30))
    level = Column(db.String(length=30))
    status = Column(db.String(length=30))
    cd_entries = relationship('ApDocCostDistribution',
                              backref='apdoc',
                              lazy='dynamic')


class ApDocCostDistribution(AuditMixin, Model):
    """ Account payable document cost distribution """

    __tablename__ = 'ap_document_cd'

    apdoc_id = reference_col('ap_documents')
    cost_account_id = reference_col('cost_accounts')
    company_unit_id = reference_col('company_units')
    amount = Column(db.Numeric)
