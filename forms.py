# forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, IntegerField
from wtforms.validators import DataRequired, Email, EqualTo

class RegistrationForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    role = SelectField('Role', choices=[('student', 'Student'), ('professor', 'Professor'), ('coordinator', 'Coordinator')], validators=[DataRequired()])
    id_card = IntegerField('ID Card', validators=[DataRequired()])
    id_card_type = SelectField('ID Type', choices=[('V', 'V'), ('E', 'E'), ('P', 'P')], validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField('Confirm Password', validators=[DataRequired()])

class LoginForm(FlaskForm):
    id_card = IntegerField('ID Card', validators=[DataRequired()])
    id_card_type = SelectField('ID Type', choices=[('V', 'V'), ('E', 'E'), ('P', 'P')], validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    role = SelectField('Role', choices=[('student', 'Student'), ('professor', 'Professor'), ('coordinator', 'Coordinator')], validators=[DataRequired()])
