
import datetime
import logging
import jinja2


from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, current_app
)

bp = Blueprint('views', __name__)

log = logging.getLogger(__name__)

from . import shelterreg

def pluralize_filter(number, singular='', plural='s'):
    """ Simple jinja filter to pluralize strings """
    if number == 1:
        return singular
    else:
        return plural

def init_app(app):
    app.register_blueprint(bp)
    app.jinja_env.filters['pluralize'] = pluralize_filter


@bp.route('/newfamily', methods=['GET', 'POST'])
def newfamily():
    log.debug("in newfamily")

    #app = current_app
    #config = app.config

    return render_template('reg/family.html')
