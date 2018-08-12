# -*- coding: utf-8 -*-
"""The app module, containing the app factory function."""
from flask import Flask, render_template
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView


from apflow_flask import commands, public, users
from apflow_flask.extensions import bcrypt, cache, csrf_protect, db, debug_toolbar, login_manager, migrate, webpack
from apflow_flask.settings import ProdConfig
# from apflow_flask.models.user import User, Role, UserRoles
# from apflow_flask.models.company import CompanyUnit, CompanyUnitType
from apflow_flask.models import *


def create_app(config_object=ProdConfig):
    """An application factory, as explained here: http://flask.pocoo.org/docs/patterns/appfactories/.

    :param config_object: The configuration object to use.
    """
    app = Flask(__name__.split('.')[0])
    app.config.from_object(config_object)
    register_extensions(app)
    register_blueprints(app)
    register_errorhandlers(app)
    register_shellcontext(app)
    register_commands(app)
    register_admin_views(app)
    return app


def register_extensions(app):
    """Register Flask extensions."""
    bcrypt.init_app(app)
    cache.init_app(app)
    db.init_app(app)
    csrf_protect.init_app(app)
    login_manager.init_app(app)
    debug_toolbar.init_app(app)
    migrate.init_app(app, db)
    webpack.init_app(app)
    return None


def register_blueprints(app):
    """Register Flask blueprints."""
    app.register_blueprint(public.views.blueprint)
    app.register_blueprint(users.views.blueprint)
    return None


def register_admin_views(app):
    admin = Admin(app, name='AP Flow')
    admin.add_view(ModelView(User, db.session, category='Security'))
    admin.add_view(ModelView(Role, db.session, category='Security'))

    admin.add_view(ModelView(CompanyUnit, db.session, category='Company'))
    admin.add_view(ModelView(CompanyUnitType, db.session, category='Company'))
    admin.add_view(ModelView(CostAccount, db.session, category='Company'))

    admin.add_view(ModelView(Counterparty, db.session,
                   category='Counterparties'))
    admin.add_view(ModelView(CounterpartyNote, db.session,
                   category='Counterparties'))
    return None


def register_errorhandlers(app):
    """Register error handlers."""
    def render_error(error):
        """Render error template."""
        # If a HTTPException, pull the `code` attribute; default to 500
        error_code = getattr(error, 'code', 500)
        return render_template('{0}.html'.format(error_code)), error_code
    for errcode in [401, 404, 500]:
        app.errorhandler(errcode)(render_error)
    return None


def register_shellcontext(app):
    """Register shell context objects."""
    def shell_context():
        """Shell context objects."""
        return {
            'db': db,
            'User': User}

    app.shell_context_processor(shell_context)


def register_commands(app):
    """Register Click commands."""
    app.cli.add_command(commands.test)
    app.cli.add_command(commands.lint)
    app.cli.add_command(commands.clean)
    app.cli.add_command(commands.urls)
    app.cli.add_command(commands.apflow)
