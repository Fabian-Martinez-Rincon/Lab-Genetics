from flask_wtf import FlaskForm
from wtforms import IntegerField, SelectField, DateField, TimeField, SubmitField, StringField
from wtforms.validators import DataRequired

class RegisterTurnoForm(FlaskForm):
    id_laboratorio = StringField('Laboratorio', validators=[DataRequired()], render_kw={"readonly": True})
    id_estudio = IntegerField('ID del Estudio', validators=[DataRequired()])
    estado = IntegerField('ID del Estado', validators=[DataRequired()])
    fecha = DateField('Fecha del Turno', validators=[DataRequired()], format='%Y-%m-%d')
    hora = TimeField('Hora del Turno', validators=[DataRequired()])
    submit = SubmitField('Registrar Turno')
