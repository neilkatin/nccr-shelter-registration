
import logging
import jinja2

from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, current_app, render_template_string
)

from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField, RadioField, validators


from . import views

bp = views.bp
log = logging.getLogger(__name__)

shelterreg_template = """
{% extends 'reg/base.html' %}

{% import 'reg/forms.macro' as fm %}

{% block pagehead -%}
Shelter Registration
{%- endblock %}

{% block title -%}
Shelter Registration
{%- endblock %}

{% block body -%}

<p>Placeholder: More text to explain purpose</p>

<p>Placeholder: shelter location they are registering for</p>

<p>Please register for the shelter</p>

<div class='container-md border'>
  <form action="" method="post" novalidate class=''>
    <div class='reg_form'>
      {% for field in form %}
        {{ fm.render_field(field) }}
      {% endfor %}

    </div>

  </form>

</div>
{%- endblock %}
"""


form_accepted_template = """
{% extends 'reg/base.html' %}

{% block pagehead -%}
Shelter Registration Accepted
{%- endblock %}

{% block title -%}
Shelter Registration Accepted
{%- endblock %}

{% block body -%}
<p>Thanks for the form.  We need more explicit text here...</p>
{%- endblock %}
"""

yes_no_choices = [ ('yes', 'Yes'), ('no', 'No') ]

class ShelterRegForm(FlaskForm):

    family_name = StringField(u'Family Name (Last Name)')
    pre_disaster_address = StringField(u'Pre Disaster Address')
    post_disaster_address = StringField(u'Post Disaster Address (if different)')
    primary_phone = StringField(u'Primary Phone')
    other_phone = StringField(u'Other Phone')
    email = StringField(u'Email')
    primary_language = StringField(u'Primary Language')
    alternate_english_speaker = StringField(u'If not English, Family Member Present Who Speaks English')
    method_of_transportation = StringField(u'Method of Transportation')
    license_plate = StringField(u'If Personal Vehicle: State + License Plate (for security purposes only)')
    required_to_register = RadioField(u'Someone in the household is required by law to register with a state or local government agency', choices=yes_no_choices)
    veteran_in_household = RadioField(u'Someone in the household is a veteran or active military', choices=yes_no_choices)
    agree_to_sharing = RadioField(u'I agree to have my information shared with other agencies providing disaster relief services', choices=yes_no_choices)
    submit = SubmitField(u'Register')
    
    


@bp.route('/shelterreg', methods=['GET', 'POST'])
def shelterreg():
    log.debug("in shelterreg")

    form = ShelterRegForm(request.form)

    if request.method == 'POST' and form.validate:
        # form accepted... do something

        return redirect(url_for('.form_accepted'))

    #app = current_app
    #config = app.config

    log.debug(f"submit label: { form.submit.label }")

    return render_template_string(shelterreg_template, form=form)


@bp.route('/shelterreg_ok', methods=['GET', 'POST'])
def form_accepted():
    return render_template_string(form_accepted_template)

