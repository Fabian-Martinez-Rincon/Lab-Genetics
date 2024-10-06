from src.core.models.database import db

class Resultado(db.Model):
    __tablename__="resultados"
    id = db.Column(db.Integer, primary_key=True, unique= True)  
    resultadoDetalle = db.Column(db.String(255), nullable=False, unique= True) #Viene de la API lo tomamos como string por ahora
    hallazgos = db.Column(db.String(255), nullable=True, unique= True)
    observacion = db.Column(db.String(255), nullable=True, unique= True)