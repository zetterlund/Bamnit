from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, SelectMultipleField
from wtforms.validators import DataRequired, ValidationError, Length
from app.models import User
from flask import request
from flask_babel import _, lazy_gettext as _l

from app.notifications import notification_helper



class EditProfileForm(FlaskForm):
    username = StringField(_l('Username'), validators=[DataRequired()])
    submit = SubmitField(_l('Submit'))

    def __init__(self, original_username, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=self.username.data).first()
            if user is not None:
                raise ValidationError('Please use a different username')



class PostForm(FlaskForm):
    post = TextAreaField(_l('Say something'), validators=[DataRequired(), Length(min=1, max=140)])
    submit = SubmitField(_l('Submit'))



class NotificationForm(FlaskForm):
    labels = notification_helper.get_field_dict()
    label = StringField('Label', validators=[DataRequired(), Length(min=1, max=256)], render_kw={"placeholder": "Name your Notification!"})
    grade = SelectMultipleField('Grade', choices=labels['grade'], default=('---ANY---', '---ANY---'))
    subject = SelectMultipleField('Subject', choices=labels['subject'], default=('---ANY---', '---ANY---'))
    language = SelectMultipleField('Language', choices=labels['language'], default=('---ANY---', '---ANY---'))
    campus = SelectMultipleField('Campus', choices=labels['campus'], default=('---ANY---', '---ANY---'))
    submit = SubmitField('Add Notification')

def get_notification_form():
    labels = notification_helper.get_field_dict()
    t1 = ('grade', SelectMultipleField('Grade', choices=labels['grade'], default=('---ANY---', '---ANY---')))
    t2 = ('subject', SelectMultipleField('Subject', choices=labels['subject'], default=('---ANY---', '---ANY---')))
    t3 = ('language', SelectMultipleField('Language', choices=labels['language'], default=('---ANY---', '---ANY---')))
    t4 = ('campus', SelectMultipleField('Campus', choices=labels['campus'], default=('---ANY---', '---ANY---')))
    form = NotificationForm()
    form._unbound_fields[1] = t1
    form._unbound_fields[2] = t2
    form._unbound_fields[3] = t3
    form._unbound_fields[4] = t4
    return form
