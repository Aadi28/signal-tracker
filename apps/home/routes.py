# -*- encoding: utf-8 -*-
from apps.home import blueprint
from flask import render_template, request, session, redirect, url_for
from flask_login import login_required
from jinja2 import TemplateNotFound
from apps import db
from apps.authentication.models import Signal, Signal_Tracking
from apps.authentication.forms import NewSignalForm

@blueprint.route('/index')
@login_required
def index():
    # user_id = session['user_id']
    user_type = session['user_type']
    tracking_data = []
    signal_list = []
    show_action_buttons = True
    
    if user_type not in ['TOS', 'TCS', 'ROUTER', 'HMO', 'CYO']:
        show_action_buttons = False

    if show_action_buttons:
        tracking_data = db.session.query(Signal_Tracking).filter_by(held_with = user_type).all()
        for tracking in tracking_data:
            temp_signal = db.session.query(Signal).filter_by(id = tracking.signal_id).first()
            temp_signal['status'] = tracking.status
            temp_signal['held_with'] = tracking.held_with
            temp_signal['tracking_id'] = tracking.tracking_id
            signal_list.append(temp_signal)
    
    if user_type == 'SUPERVISOR': 
        signal_list = db.session.query(Signal).filter_by().all()
        for signal in signal_list:
            signal_track = db.session.query(Signal_Tracking).filter_by(signal_id = signal.id).first()
            signal['status'] = signal_track.status
            signal['held_with'] = signal_track.held_with
            signal['tracking_id'] = signal_track.tracking_id

    return render_template('home/tables.html', segment='signals', table_data=signal_list)
  

@blueprint.route('/enterDetails', methods=['GET', 'POST'])
@login_required
def enterDetails():
    new_signal_form = NewSignalForm(request.form)
    signal_list = db.session.query(Signal).filter_by().all()
    tracker_list = db.session.query(Signal_Tracking).filter_by().all()
    if 'enterDetails' in request.form:
        record = Signal(**request.form)
        tracking = Signal_Tracking()
        
        if not tracker_list:
            tracking['tracking_id'] = 1
        else:
            tracking['tracking_id'] = tracker_list[-1].tracking_id + 1
        
        if not signal_list:
            record['id'] = 1
        else:
            record['id'] = signal_list[-1].id + 1

        tracking['status'] = 'INITIATED'
        tracking['held_with'] = 'TOS'
        tracking['signal_id'] = record['id']
        record['tracking_id'] = tracking['tracking_id']
        
        db.session.add(record)
        db.session.add(tracking)
        db.session.commit()
        
        return render_template('home/enterDetails.html', success=True, form = new_signal_form)
    else:
        return render_template('home/enterDetails.html', success=False, form = new_signal_form)


@blueprint.route('/forward_tcs', methods=['POST'])
def forwardTcs():
    signal = request.get_json()
    signal_track = db.session.query(Signal_Tracking).filter_by(signal_id = signal['id']).first()
    signal_track['held_with'] = 'TCS'
    db.session.commit()
    index()
    return redirect('/index')


@blueprint.route('/forward_hmo', methods=['POST'])
def forwardHmo():
    signal = request.get_json()
    signal_track = db.session.query(Signal_Tracking).filter_by(signal_id = signal['id']).first()
    signal_track['held_with'] = 'HMO'
    signal_track['status'] = 'APPROVED'
    db.session.commit()
    return redirect(url_for('home_blueprint.index'))

@blueprint.route('/forward_cyo', methods=['POST'])
def forwardCyo():
    signal = request.get_json()
    signal_track = db.session.query(Signal_Tracking).filter_by(signal_id = signal['id']).first()
    signal_track['held_with'] = 'CYO'
    db.session.commit()
    return redirect(url_for('home_blueprint.index'))

@blueprint.route('/forward_router', methods=['POST'])
def forwardRouter():
    signal = request.get_json()
    signal_track = db.session.query(Signal_Tracking).filter_by(signal_id = signal['id']).first()
    signal_track['held_with'] = 'ROUTER'
    db.session.commit()
    return redirect(url_for('home_blueprint.index'))


@blueprint.route('/dispatched', methods=['POST'])
def dispatched():
    signal = request.get_json()
    signal_track = db.session.query(Signal_Tracking).filter_by(signal_id = signal['id']).first()
    signal_track['status'] = 'DISPATCHED'
    db.session.commit()
    return redirect(url_for('home_blueprint.index'))


@blueprint.route('/distributed', methods=['POST'])
def distributed():
    signal = request.get_json()
    signal_track = db.session.query(Signal_Tracking).filter_by(signal_id = signal['id']).first()
    signal_track['status'] = 'DISTRIBUTED'
    db.session.commit()
    return redirect(url_for('home_blueprint.index'))

@blueprint.route('/returned', methods=['POST'])
def sentBack():
    signal = request.get_json()
    signal_track = db.session.query(Signal_Tracking).filter_by(signal_id = signal['id']).first()
    signal_track['held_with'] = 'OPERATOR'
    signal_track['status'] = 'RETURNED'
    db.session.commit()
    return redirect(url_for('home_blueprint.index'))

@blueprint.route('/new_signal', methods=['POST'])

@blueprint.route('/<template>')
@login_required
def route_template(template):

    try:

        if not template.endswith('.html'):
            template += '.html'

        # Detect the current page
        segment = get_segment(request)
        # Serve the file (if exists) from app/templates/home/FILE.html
        return render_template('home/' + template, segment=segment)

    except TemplateNotFound:
        return render_template('home/page-404.html'), 404

    except Exception:
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
