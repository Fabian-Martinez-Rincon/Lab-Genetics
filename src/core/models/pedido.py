from src.core.models.database import db

class Pedido(db.Model):
    __tablename__="pedidos"
    id = db.Column(db.Integer, primary_key=True, unique= True)
    estudios = db.relationship('Estudio', backref='estudios', cascade='all, delete-orphan')
    id_laboratorio = db.Column(db.Integer, db.ForeignKey("laboratorios.id"), nullable=False)
    estado = db.Column(db.String(50), nullable=False) #Pendiente, En proceso, Finalizado, Cancelado
    observaciones = db.Column(db.String(255), nullable=True) #Observaciones del Cancelado/Rechazado
    