from wtforms import (
    BooleanField,
    TextField,
    TextAreaField,
    PasswordField,
    validators,
    SubmitField,
    FileField
)
from flask.ext.wtf import Form


class SetupForm(Form):
    site_name = TextField('Site Name', [validators.Length(min=4, max=35)])
    db_name = TextField('Database Name', [validators.Length(min=4, max=25)])
    password = PasswordField('New Password', [
        validators.Required(),
        validators.EqualTo('password_confirm', message='Passwords must match')
    ])
    password_confirm = PasswordField('Repeat Password')
    submit = SubmitField('Create')


class UploadFileForm(Form):
    file = FileField('File')
    title = TextField('Title', [validators.Length(min=4, max=256)])
    submit = SubmitField('Upload')


class PostForm(Form):
    title = TextField('Title', [validators.Length(min=4, max=256)])
    content = TextAreaField('Content', [validators.Length(min=4, max=1024)])
    submit = SubmitField('Publish')
