from flask import render_template, flash, redirect, url_for, request, g, current_app
from app import db
from flask_login import current_user, login_required
from app.models import User, Listing, Notification
from app.notifications import notification_helper
from app.analysis.analysis_helper import get_weekday_count, get_time_available, grade_list
from werkzeug.urls import url_parse
from datetime import datetime, time
from flask_babel import _, get_locale
from app.main.forms import EditProfileForm, get_notification_form
from app.main import bp


@bp.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()
    g.locale = str(get_locale())


@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index', methods=['GET', 'POST'])
def index():
    
    weekday_count = get_weekday_count()
    time_available = get_time_available()
    d = {}
    d['g1'] = {}
    d['g1']['legend'] = 'Legend1'
    d['g1']['labels'] = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
    d['g1']['values'] = weekday_count
    d['g2'] = {}
    d['g2']['legend'] = 'Time Available'
    d['g2']['labels'] = grade_list
    d['g2']['values'] = time_available

    if current_user.is_authenticated:
        user = current_user
        page = request.args.get('page', 1, type=int)
        notifications = user.notifications.order_by(Notification.timestamp.desc()).paginate(page, current_app.config['POSTS_PER_PAGE'], False)
        next_url = url_for('main.index', username=user.username, page=notifications.next_num) if notifications.has_next else None
        prev_url = url_for('main.index', username=user.username, page=notifications.prev_num) if notifications.has_prev else None
        n_strings = notification_helper.get_strings(notifications.items)
        return render_template('dashboard.html',
                               d=d,
                               heading="Dashboard",
                               user=user,
                               next_url=next_url,
                               prev_url=prev_url,
                               notifications=notifications.items,
                               n_strings=n_strings,
                               )

    else:
        return render_template('index.html',
                               heading="Welcome",
                               d=d)


@bp.route('/about', methods=['GET', 'POST'])
def about():
    return render_template('about.html',
                           heading="About")


@bp.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        db.session.commit()
        flash(_('Your changes have been saved.'))
        return redirect(url_for('main.edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
    return render_template('edit_profile.html',
                           title=_('Edit Profile'),
                           heading="Edit Profile",
                           form=form)


@bp.route('/remove_notification/<notification_id>', methods=['GET', 'POST'])
@login_required
def remove_notification(notification_id):
    notification = Notification.query.filter_by(id=notification_id).first()
    if notification.receiver == current_user:
        db.session.delete(notification)
        db.session.commit()
        flash('Notification \'{}\' deleted!'.format(notification.label))
        return redirect(url_for('main.index'))
    else:
        flash('This is not your notification!')
        return redirect(url_for('main.index'))


@bp.route('/notifications', methods=['GET', 'POST'])
# @login_required
def notifications():
    form = get_notification_form()
    if form.validate_on_submit():
        notification = Notification(label=form.label.data,
                                    grade=str(form.grade.data),
                                    subject=str(form.subject.data),
                                    language=str(form.language.data),
                                    campus=str(form.campus.data),
                                    receiver=current_user)
        db.session.add(notification)
        db.session.commit()        
        flash('Notification \'{}\' has been added!'.format(form.label.data))
        return redirect(url_for('main.index', username=current_user.username))
    return render_template('notifications.html',
                           heading="Add Notification",
                           form=form)


@bp.route('/get_toggled_status', methods=['GET', 'POST']) 
def toggled_status():
    current_status = request.args.get('status')
    if current_status == 'OFF':
        current_user.notifications_enabled = True
        db.session.commit()
        return 'ON'
    else:
        current_user.notifications_enabled = False
        db.session.commit()
        return 'OFF'


@bp.route('/api', methods=['GET'])
def api():
    return render_template('api.html',
                           heading="API")