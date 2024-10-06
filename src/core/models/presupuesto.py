from src.core.models.database import db

class Presupuesto(db.Model):
    __tablename__="presupuestos"
    id = db.Column(db.Integer, primary_key=True, unique= True)
    fecha_vencimiento = db.Column(db.Date, nullable=True)
    Detalle = db.Column(db.String(255), nullable=False, unique= True) #Texto con todo el detalle de lo que se va a hacer y el precio de cada cosa
    montoFinal = db.Column(db.Float, nullable=False)