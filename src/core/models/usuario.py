from flask_login import UserMixin
from src.core.models.database import db

class Usuario(UserMixin, db.Model):
    __tablename__ = "usuarios"
    id               = db.Column(db.Integer, primary_key=True, unique=True)
    nombre           = db.Column(db.String(50), nullable=False)
    apellido         = db.Column(db.String(50), nullable=False)
    password         = db.Column(db.String(255), nullable=False)
    email            = db.Column(db.String(255), nullable=False, unique=True)
    dni              = db.Column(db.String(12), nullable=False, unique=True)
    fecha_nacimiento = db.Column(db.Date, nullable=False)
    telefono         = db.Column(db.String(50), nullable=False)
    historia_path    = db.Column(db.String(255), nullable=True)
    id_rol = db.Column(db.Integer, db.ForeignKey("roles.id"), nullable=False)
    id_medico = db.Column(db.Integer, db.ForeignKey("usuarios.id"), nullable=True)
    turnos = db.relationship('Turno', backref='turnos', cascade='all, delete-orphan') 
    estado = db.Column(db.String(50), default = 'ACTIVO') #Activo - Inactivo
    # Relación con los estudios como paciente
    estudios_como_paciente = db.relationship('Estudio', backref='paciente', foreign_keys='Estudio.id_paciente', cascade='all, delete-orphan')
    # Relación con los estudios como médico
    estudios_como_medico = db.relationship('Estudio', backref='medico', foreign_keys='Estudio.id_medico', cascade='all, delete-orphan')
    patologias = db.relationship('Patologia', secondary='antecedentes_usuarios', backref='usuarios')
     
# Tabla intermedia para la relación muchos a muchos entre Usuario y Antecedentes Familiares
antecedentes_usuarios = db.Table('antecedentes_usuarios',
    db.Column('usuario_id', db.Integer, db.ForeignKey('usuarios.id'), primary_key=True),
    db.Column('patologia_id', db.Integer, db.ForeignKey('patologias.id'), primary_key=True)
)
