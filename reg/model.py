#
# models for shelterreg project
#

import logging
import datetime
from dateutil.tz import tzutc, gettz

import sqlalchemy
import enum

from sqlalchemy import Column, ForeignKey, Integer, String, BigInteger, TIMESTAMP, desc, Boolean, Date, DateTime, orm, types, UniqueConstraint
from sqlalchemy.dialects import mysql, sqlite

from sqlalchemy.orm import relationship
from sqlalchemy.sql import functions as func

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


log = logging.getLogger(__name__)

db = SQLAlchemy()
migrate = Migrate()

# tiny utility functions
def get_db():
    return db

def session():
    return db.session;



# mixin to set 'normal' table defaults
class TableMixin(object):

    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8mb4',
    }


# type decorator so all db time is UTC
CurrentTZ = gettz(name=None)
class UTCDateTime(types.TypeDecorator):
    impl = types.DateTime

    def process_bind_param(self, value, engine):
        if value is not None:
            if value.tzinfo is None:
                new = value.replace(tzinfo=CurrentTZ)
                return value.astimezone(tzutc())
            else:
                return value.astimezone(tzutc())

    def process_result_value(self, value, engine):
        if value is not None:
            return datetime(value.year, value.month, value.day,
                            value.hour, value.minute, value.second,
                            value.microsecond, tzinfo=tzutc())


MyBigInt = BigInteger().  with_variant(sqlite.INTEGER(), 'sqlite').  with_variant(mysql.BIGINT(), 'mysql')

class Family(TableMixin, db.Model):
    __tablename__ = "families"

    id = Column(MyBigInt, primary_key=True)

    first = Column(String(100), nullable=False)
    last = Column(String(100), nullable=False)
    mobile = Column(String(50), nullable=False)
    email = Column(String(256), nullable=False)
    family_size = Column(Integer(), nullable=False)


# helper app to make schema migration of booleans work with alembic
def alembic_compare_type(context, inspected_column, metadata_column, inspected_type, metadata_type):
    if isinstance(inspected_type, sqlalchemy.dialects.mysql.TINYINT) and isinstance(metadata_type, sqlalchemy.Boolean):
        return False
    else:
        return None


def init_app(app):
    log.debug(f"init_app: called.  db { db }")

    db.init_app(app)
    migrate.init_app(app, db, compare_type=alembic_compare_type)

