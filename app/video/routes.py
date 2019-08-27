from flask import render_template, redirect, url_for, flash, request
from werkzeug.urls import url_parse
from flask_login import login_user, logout_user, current_user
from flask_babel import _
from app import db
from app.video import bp
# from app.auth.forms import LoginForm, RegistrationForm, ResetPasswordRequestForm, ResetPasswordForm
# from app.models import User
# from app.auth.email import send_password_reset_email


@bp.route('/chat', methods=['GET', 'POST'])
def index():
    return render_template('video/chat.html',
                           title=_('Video Chat'),
                           heading="Video Chat")
