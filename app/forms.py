from wtforms import Form, BooleanField, StringField, PasswordField, validators


class RegistrationForm(Form):
    name = StringField('Name', validators=[validators.Length(min=4, max=25)])

    username = StringField('Username', validators=[validators.input_required(), validators.Length(min=4, max=25)])

    email = StringField('Email Address', [validators.Length(min=6, max=35)])

    password = PasswordField('New Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])

    confirm = PasswordField('Repeat Password')
    # accept_tos = BooleanField('I accept the TOS', [validators.DataRequired()])


# so inside this called, all conditions must be met for the form to validate.
# it was noticed that once one is not met or not included in the html form field, it doesn't validate


class ArticleForm(Form):
    title = StringField('Title', validators=[validators.Length(min=1, max=250)])

    body = StringField('Body', validators=[validators.input_required(), validators.Length(min=1, max=2500)])
