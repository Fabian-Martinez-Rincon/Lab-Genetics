from flask_login import UserMixin
from src.core.models.database import db

class Usuario(UserMixin, db.Model):
    __tablename__ = "usuarios"
    id = db.Column(db.Integer, primary_key=True, unique=True)
    nombre = db.Column(db.String(50), nullable=False)
    apellido = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    dni = db.Column(db.String(12), nullable=True, unique=True)
    fecha_nacimiento = db.Column(db.Date, nullable=True)
    telefono = db.Column(db.String(50), nullable=True)
    historia_path = db.Column(db.String(255), nullable=False)
    antecedentes = db.relationship('Patologia', backref='patologias', cascade='all, delete-orphan')
    id_rol = db.Column(db.Integer, db.ForeignKey("roles.id"), nullable=False)
    id_medico = db.Column(db.Integer, db.ForeignKey("usuarios.id"), nullable=False)
    estudios = db.relationship('Estudio', backref='estudios', cascade='all, delete-orphan')
    turnos = db.relationship('Turno', backref='turnos', cascade='all, delete-orphan')