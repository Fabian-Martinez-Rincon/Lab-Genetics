from datetime import datetime
from src.core.models.database import db

class HistorialEstado(db.Model):
    __tablename__ = "historial_estados"
    id = db.Column(db.Integer, primary_key=True)
    estudio_id = db.Column(db.String(255), db.ForeignKey("estudios.id"), nullable=False)
    estado = db.Column(db.String(50), nullable=False)
    fecha_hora = db.Column(db.DateTime, default=datetime.now)
    
