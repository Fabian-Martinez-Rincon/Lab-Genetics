from src.core.models.database import db
from datetime import datetime
class Exterior(db.Model):
    __tablename__="exteriors"
    id = db.Column(db.Integer, primary_key=True, unique= True)
    estudios = db.relationship('Estudio', backref='exterior_relacion', cascade='all, delete-orphan')
    fecha_envio = db.Column(db.DateTime, default=datetime.now)
    estado = db.Column(db.String(100), nullable=False) #ENVIADO AL EXTERIOR, RESULTADOS RECIBIDOS