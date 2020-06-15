
from flask import current_app, g
from flask.cli import with_appcontext
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

import sqlalchemy
import sqlalchemy.dialects.mysql

import logging

import click

log = logging.getLogger(__name__)


from .model import get_db

def init_app(app):
    log.debug("init_app: called")

    app.cli.add_command(db_reset)
    app.cli.add_command(db_create)


# cli commands

@click.command('db-reset')
@with_appcontext
def db_reset():
    app = current_app
    log.info("db-reset called: resetting all db tables")

    db = get_db()
    db.drop_all()
    db.create_all()

@click.command('db-create')
@with_appcontext
def db_create():
    app = current_app
    db = get_db()

    log.info("db-create called: creating all db tables")
    db.create_all()
