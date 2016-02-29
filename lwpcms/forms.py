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
    user_name = TextField('User Name', [validators.Length(min=4, max=35)])
    password = PasswordField('Choose Password', [
        validators.Required(),
        validators.EqualTo('password_confirm', message='Passwords must match')
    ])
    password_confirm = PasswordField('Repeat Password')
    demo = BooleanField('Demo')
    submit = SubmitField('Create')


class LoginForm(Form):
    user_name = TextField('User Name', [validators.Length(min=4, max=35)])
    password = PasswordField('Password', [
        validators.Required()
    ])
    submit = SubmitField('Login')


class UploadFileForm(Form):
    file = FileField('File')
    title = TextField('Title', [validators.Length(min=4, max=256)])
    submit = SubmitField('Upload')


class PostForm(Form):
    title = TextField('Title', [validators.Length(min=4, max=256)])
    content = TextAreaField('Body', [validators.Length(min=4, max=100000)])
    submit = SubmitField('Publish')
    update = SubmitField('Update')


class SettingsForm(Form):
    demo = SetupForm.demo
    site_name = SetupForm.site_name
    site_description = TextAreaField('Site Description', [validators.Length(min=4, max=100000)])
    submit = SubmitField('Save')
