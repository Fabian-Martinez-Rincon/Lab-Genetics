from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField, SelectMultipleField, FileField
from wtforms.validators import DataRequired, Length, Optional, Email, ValidationError
from flask_wtf.file import FileAllowed, FileRequired
import datetime

class RegisterPacienteForm(FlaskForm):
    nombre = StringField('Nombre', validators=[DataRequired(), Length(max=50)])
    apellido = StringField('Apellido', validators=[DataRequired(), Length(max=50)])
    email = StringField('Email', validators=[
        DataRequired(message="Este campo es obligatorio."),
        Email(message="Por favor ingrese un correo electrónico válido.")
    ])
    dni = StringField('DNI', validators=[Optional(), Length(min=8)])
    fecha_nacimiento = DateField('Fecha de Nacimiento', validators=[DataRequired()], format='%Y-%m-%d')
    telefono = StringField('Teléfono', validators=[Optional(), Length(max=50)])

    patologias = SelectMultipleField('Patologías', coerce=int, validators=[DataRequired()])
    historia = FileField('Historia Clínica (PDF)', validators=[
        FileRequired(),
        FileAllowed(['pdf'], 'Solo se permiten archivos PDF.')
    ])
    
    submit = SubmitField('Registrar Paciente')

    def validate_fecha_nacimiento(self, field):
        """Valida que la fecha de nacimiento sea anterior a la fecha actual."""
        if field.data >= datetime.date.today():
            raise ValidationError("La fecha de nacimiento debe ser anterior a la fecha de hoy.")

    def validate_relacion(self, field):
        """Valida que se ingrese un parentesco si se seleccionó la patología correspondiente."""
        for id in self.patologias.data:
            relacion_field = getattr(self, f'relation_{id}', None)
            if relacion_field and not relacion_field.data.strip():
                raise ValidationError(f"Debe ingresar el parentesco para la patología seleccionada con ID {id}.")

