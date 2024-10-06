from src.core.models.database import db

class Patologia(db.Model):
    __tablename__="patologias"
    id = db.Column(db.Integer, primary_key=True, unique= True)
    nombre = db.Column(db.String(50), nullable=False, unique= True)