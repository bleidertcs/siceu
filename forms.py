# forms.py
# Importamos FlaskForm para crear formularios
from flask_wtf import FlaskForm
# Importamos los tipos de campos que usaremos en los formularios
from wtforms import StringField, PasswordField, SelectField, IntegerField
# Importamos los validadores para los campos
from wtforms.validators import DataRequired, Email, EqualTo

# Definimos una clase RegistrationForm que hereda de FlaskForm
class RegistrationForm(FlaskForm):
    # Cada atributo de la clase RegistrationForm representa un campo del formulario
    
    # Campo para el nombre del usuario
    name = StringField('Nombre', validators=[DataRequired()]) 
    # validators=[DataRequired()] indica que este campo es obligatorio

    # Campo para el apellido del usuario
    last_name = StringField('Apellido', validators=[DataRequired()])
    # validators=[DataRequired()] indica que este campo es obligatorio

    # Campo para seleccionar el rol del usuario
    role = SelectField('Rol', choices=[('estudiante', 'Estudiante'), ('profesor', 'Profesor'), ('coordinador', 'Coordinador')], validators=[DataRequired()])
    # choices define las opciones disponibles en el select, validators=[DataRequired()] indica que este campo es obligatorio

    # Campo para la cédula del usuario
    id_card = IntegerField('Cedula', validators=[DataRequired()])
    # validators=[DataRequired()] indica que este campo es obligatorio

    # Campo para seleccionar el tipo de documento del usuario
    id_card_type = SelectField('Tipo de documento', choices=[('V', 'V'), ('E', 'E'), ('P', 'P')], validators=[DataRequired()])
    # choices define las opciones disponibles en el select, validators=[DataRequired()] indica que este campo es obligatorio

    # Campo para el correo electrónico del usuario
    email = StringField('Correo', validators=[DataRequired(), Email()])
    # validators=[DataRequired(), Email()] indica que este campo es obligatorio 
    # y que debe contener un correo electrónico válido

    # Campo para la contraseña del usuario
    password = PasswordField('Contraseña', validators=[DataRequired(), EqualTo('confirm', message='Las contraseñas no coinciden')])
    # validators=[DataRequired(), EqualTo('confirm', message='Las contraseñas no coinciden')] 
    # indica que este campo es obligatorio y que debe coincidir con el valor del campo 'confirm'

    # Campo para confirmar la contraseña del usuario
    confirm = PasswordField('Confirmar Contraseña', validators=[DataRequired()])
    # validators=[DataRequired()] indica que este campo es obligatorio


# Definimos una clase LoginForm que hereda de FlaskForm
class LoginForm(FlaskForm):
    # Cada atributo de la clase LoginForm representa un campo del formulario

    # Campo para la cédula del usuario
    id_card = IntegerField('Cedula', validators=[DataRequired()])
    # validators=[DataRequired()] indica que este campo es obligatorio

    # Campo para seleccionar el tipo de documento del usuario
    id_card_type = SelectField('Tipo de documento', choices=[('V', 'V'), ('E', 'E'), ('P', 'P')], validators=[DataRequired()])
    # choices define las opciones disponibles en el select, validators=[DataRequired()] indica que este campo es obligatorio

    # Campo para la contraseña del usuario
    password = PasswordField('Contraseña', validators=[DataRequired()])
    # validators=[DataRequired()] indica que este campo es obligatorio

    # Campo para seleccionar el rol del usuario
    role = SelectField('Rol', choices=[('estudiante', 'Estudiante'), ('profesor', 'Profesor'), ('coordinador', 'Coordinador')], validators=[DataRequired()])
    # choices define las opciones disponibles en el select, validators=[DataRequired()] indica que este campo es obligatorio
