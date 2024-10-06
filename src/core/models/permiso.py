from src.core.models.database import db

class Permiso(db.Model):
    __tablename__="permisos"
    id = db.Column(db.Integer, primary_key=True, unique= True)
    nombre = db.Column(db.String(50), nullable=False, unique= True)
    id_rol = db.Column(db.Integer, db.ForeignKey("roles.id"), nullable=False)