from wtforms import Form, BooleanField, TextField, PasswordField, validators, SubmitField


class SetupForm(Form):
    site_name = TextField('Site Name', [validators.Length(min=4, max=35)])
    db_name = TextField('Database Name', [validators.Length(min=4, max=25)])
    password = PasswordField('New Password', [
        validators.Required(),
        validators.EqualTo('password_confirm', message='Passwords must match')
    ])
    password_confirm = PasswordField('Repeat Password')
    submit = SubmitField('Create')
