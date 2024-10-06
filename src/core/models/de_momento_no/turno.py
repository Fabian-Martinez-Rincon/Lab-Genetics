from src.core.models.database import db

class Turno(db.Model):
    __tablename__="turnos"
    id = db.Column(db.Integer, primary_key=True, unique= True)
    id_paciente = db.Column(db.Integer, db.ForeignKey("usuarios.id"), nullable=False)
    id_laboratorio = db.Column(db.Integer, db.ForeignKey("usuarios.id"), nullable=False)
    fecha = db.Column(db.Date, nullable=False)
    hora = db.Column(db.Time, nullable=False)