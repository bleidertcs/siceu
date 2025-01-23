# forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, IntegerField
from wtforms.validators import DataRequired, Email, EqualTo

class RegistrationForm(FlaskForm):
    name = StringField('Nombre', validators=[DataRequired()])
    last_name = StringField('Apellido', validators=[DataRequired()])
    role = SelectField('Rol', choices=[('estudiante', 'Estudiante'), ('profesor', 'Profesor'), ('coordinador', 'Coordinador')], validators=[DataRequired()])
    id_card = IntegerField('Cedula', validators=[DataRequired()])
    id_card_type = SelectField('Tipo de documento', choices=[('V', 'V'), ('E', 'E'), ('P', 'P')], validators=[DataRequired()])
    email = StringField('Correo', validators=[DataRequired(), Email()])
    password = PasswordField('Contraseña', validators=[DataRequired(), EqualTo('confirm', message='Las contraseñas no coinciden')])
    confirm = PasswordField('Confirmar Contraseña', validators=[DataRequired()])

class LoginForm(FlaskForm):
    id_card = IntegerField('Cedula', validators=[DataRequired()])
    id_card_type = SelectField('Tipo de documento', choices=[('V', 'V'), ('E', 'E'), ('P', 'P')], validators=[DataRequired()])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    role = SelectField('Rol', choices=[('estudiante', 'Estudiante'), ('profesor', 'Profesor'), ('coordinador', 'Coordinador')], validators=[DataRequired()])
