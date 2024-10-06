from src.core.models.database import db

class Laboratorio(db.Model):
    __tablename__ = "laboratorios"
    id = db.Column(db.Integer, primary_key=True, unique=True)
    nombre = db.Column(db.String(255), nullable=False)
    direccion = db.Column(db.String(255), nullable=False)
    horarios = db.Column(db.String(255), nullable=False)
    dias = db.Column(db.String(255), nullable=False)
    telefono = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    #Para la ubicacion del mapa concatena longitud y latitud
    address = db.Column(db.String(255), nullable=False) 
    # id_rol = db.Column(db.Integer, db.ForeignKey("roles.id"), nullable=False)
    # turnos = db.relationship('Turno', backref='turnos', cascade='all, delete-orphan')