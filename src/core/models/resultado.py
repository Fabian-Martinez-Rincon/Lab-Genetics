from src.core.models.database import db

class Resultado(db.Model):
    __tablename__="resultados"
    id = db.Column(db.Integer, primary_key=True, unique= True)  
    resultadoBase = db.Column(db.String(255), nullable=False)
    resultadoGenesAdicionales = db.Column(db.String(255), nullable=True) 
    resultadoHallazgosSecundarios = db.Column(db.String(255), nullable=True)
    observacion = db.Column(db.String(255), nullable=True)