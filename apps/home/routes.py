# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from apps.home import blueprint
from flask import render_template, request
from flask_login import login_required
from jinja2 import TemplateNotFound
from apps import db
from apps.authentication.models import Signal, Signal_Tracking
# from ocr_pro import ocr_core

#define a folder to store and later serve the images
UPLOAD_FOLDER = '/static/Test_Images/'

#allow files of a specific type
ALLOWED_EXTENSIONS = set(['png','jpg','jpeg'])

@blueprint.route('/index')
@login_required
def index():
    signal_list = db.session.query(Signal).filter_by().all()
    for signal in signal_list:
        tracking_data = db.session.query(Signal_Tracking).filter_by(signal_id = signal.id).first()
        signal['status'] = tracking_data.status
        signal['held_with'] = tracking_data.held_with

    return render_template('home/tables.html', segment='signals', table_data=signal_list)


@blueprint.route('/<template>')
@login_required
def route_template(template):

    try:

        if not template.endswith('.html'):
            template += '.html'

        # Detect the current page
        segment = get_segment(request)

        # Serve the file (if exists) from app/templates/home/FILE.html
        return render_template("home/" + template, segment=segment)

    except TemplateNotFound:
        return render_template('home/page-404.html'), 404

    except:
        return render_template('home/page-500.html'), 500


# Helper - Extract current page name from request
def get_segment(request):

    try:

        segment = request.path.split('/')[-1]

        if segment == '':
            segment = 'index'

        return segment

    except:
        return None
