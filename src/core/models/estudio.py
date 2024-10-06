from datetime import datetime
from src.core.models.database import db

class Estudio(db.Model):
    __tablename__="estudios"
    id = db.Column(db.Integer, primary_key=True, unique= True)
    id_paciente = db.Column(db.Integer, db.ForeignKey("usuarios.id"), nullable=False)  
    id_medico = db.Column(db.Integer, db.ForeignKey("usuarios.id"), nullable=False)
    sintomas = db.Column(db.String(255), nullable=True) #viene de la API y se carga como string ¿? Hasta que sepamos que datos le tenemos que enviar a la api que evalua la patologia
    listado_genes = db.Column(db.String(255), nullable=True) #viene de la API si selecciono sintomas
    hallazgos_secundarios = db.Column(db.Boolean, default=False)
    fecha_solicitud = db.Column(db.DateTime, default=datetime.now)
    fecha_ingreso_central = db.Column(db.Date, nullable=True)
    id_estado = db.Column(db.Integer, db.ForeignKey("estados.id"), nullable=False)
    id_resultado = db.Column(db.Integer, db.ForeignKey("resultados.id"), nullable=False)
    id_presupuesto = db.Column(db.Integer, db.ForeignKey("presupuestos.id"), nullable=False)
    comprobante_path = db.Column(db.String(255), nullable=False) #Hay que decidir si va a ser una foto o PDF
    # Clave foránea para vincular con Pedido
    id_pedido = db.Column(db.Integer, db.ForeignKey('pedidos.id'), nullable=True)
# Tabla intermedia para la relación muchos a muchos entre Estudios y Patologias
estudios_patologias = db.Table('estudios_patologias',
    db.Column('estudio_id', db.Integer, db.ForeignKey('estudios.id'), primary_key=True),
    db.Column('patologia_id', db.Integer, db.ForeignKey('patologias.id'), primary_key=True)
)
