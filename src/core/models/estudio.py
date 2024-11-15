from datetime import datetime
from src.core.models.database import db

class Estudio(db.Model):
    __tablename__ = "estudios"
    id = db.Column(db.String(255), primary_key=True, unique=True)
    id_paciente = db.Column(db.Integer, db.ForeignKey("usuarios.id"), nullable=False)  
    id_medico = db.Column(db.Integer, db.ForeignKey("usuarios.id"), nullable=False)
    tipo_estudio = db.Column(db.String(50), nullable=False)  # Familiar o Puntual
    sintomas = db.Column(db.String(255), nullable=True)
    listado_genes = db.Column(db.String(255), nullable=True)
    genes_adicionales = db.Column(db.String(255), nullable=True)
    hallazgos_secundarios = db.Column(db.Boolean, default=False)
    fecha_solicitud = db.Column(db.DateTime, default=datetime.now)
    fecha_ingreso_central = db.Column(db.Date, nullable=True)
    id_resultado = db.Column(db.Integer, db.ForeignKey("resultados.id"), nullable=True)
    id_presupuesto = db.Column(db.Integer, db.ForeignKey("presupuestos.id"), nullable=True)
    comprobante_path = db.Column(db.String(255), nullable=True) #Hay que decidir si va a ser una foto o PDF
    # Clave foránea para vincular con Pedido
    id_pedido = db.Column(db.Integer, db.ForeignKey('pedidos.id'), nullable=True)
    # Historial de estados
    historial = db.relationship("HistorialEstado", backref="estudio_relacion", cascade="all, delete-orphan")
    patologias = db.relationship('Patologia', secondary='estudios_patologias', back_populates='estudios')
    
    @classmethod
    def generar_id(cls, apellido, nombre, id_paciente):
        apellido_abrev = apellido[:3].upper()
        nombre_abrev = nombre[:3].upper()
        numero = f"{len(cls.query.filter_by(id_paciente=id_paciente).all()) + 1:03d}"
        return f"{apellido_abrev}_{nombre_abrev}_{numero}"


   # Tabla intermedia para la relación muchos a muchos entre Estudios y Patologias
    estudios_patologias = db.Table('estudios_patologias',
        db.Column('estudio_id', db.String(255), db.ForeignKey('estudios.id'), primary_key=True),
        db.Column('patologia_id', db.Integer, db.ForeignKey('patologias.id'), primary_key=True)
    )