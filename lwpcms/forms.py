from wtforms import (Form,
    BooleanField,
    TextField,
    PasswordField,
    validators,
    SubmitField,
    FileField
)


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
    description = TextField('Description',
            [validators.Length(min=4, max=1024)])
    submit = SubmitField('Upload')
