""" Initalize db with some data for development purposes. """
import os
import yaml
from apflow_flask.models import User
from apflow_flask.models import CompanyUnitType, CompanyUnit
from apflow_flask.models import DocType
from apflow_flask.models import Counterparty

class DevDataImport:
    def __init__(self, db, yaml_fname):
        self.db = db
        self.yaml_fname = yaml_fname
        self.data = self.get_yaml_data()

    def get_yaml_data(self):
        with open(self.yaml_fname, 'r') as f:
            data = yaml.load(f)
        return data

    def get_unit_types_dict(self):
        return {v: k for k, v in enumerate(self.data['unit_types'], 1)}

    def create_dev_admin(self):
        """ Creates admin user. """
        admin = User(**self.data['users']['admin'])
        self.db.session.add(admin)
        self.db.session.commit()

    def create_unit_types(self):
        for ut in self.data['unit_types']:
            unit = CompanyUnitType(name=ut, created_by=1, updated_by=1)
            self.db.session.add(unit)
            # import pdb; pdb.set_trace()
        self.db.session.commit()

    def create_ap_document_types(self):
        for dt in self.data['ap_document_types']:
            doc = DocType(type_name=dt, created_by=1, updated_by=1)
            self.db.session.add(doc)
        self.db.session.commit()

    def create_company_units(self):
        """ Creates company units """
        ut_dict = self.get_unit_types_dict()
        units_dict = {v['name']: k for k, v in enumerate(self.data['units'], 1)}
        # import pdb; pdb.set_trace()
        for u in self.data['units']:
            unit = CompanyUnit()
            unit.name = u['name']
            unit.unit_type_id = ut_dict.get(u['unit_type'])
            unit.parent_id = units_dict.get(u['parent'])
            unit.created_by = 1
            unit.updated_by = 1
            self.db.session.add(unit)
        self.db.session.commit()

    def create_counterparties(self):
        for c in self.data['counterparties']:
            counterparty = Counterparty(created_by=1, updated_by=1, **c)
            self.db.session.add(counterparty)
        self.db.session.commit()

    def run_all(self):
        self.db.drop_all()
        self.db.create_all()
        self.create_dev_admin()
        self.create_unit_types()
        self.create_company_units()
        self.create_ap_document_types()
        self.create_counterparties()
