from src.core.models.database import db

class Presupuesto(db.Model):
    __tablename__="presupuestos"
    id = db.Column(db.Integer, primary_key=True, unique= True)
    fecha_vencimiento = db.Column(db.Date, nullable=True)
    Detalle = db.Column(db.Text, nullable=False, unique= True) #Texto con todo el detalle de lo que se va a hacer y el precio de cada cosa
    montoFinal = db.Column(db.Float, nullable=False)
    comprobante_path = db.Column(db.String(255), nullable=True) #Hay que decidir si va a ser una foto o PDF
    id_estado = db.Column(db.Integer, db.ForeignKey("estados.id"), nullable=False)
    
    @classmethod
    def generar_detalle(cls, patologias, genes, adicionales, hallazgos):
        detalle = ""
        if patologias:
            detalle += f"Patologías a Evaluar: {patologias}\n"
        if genes:
            detalle += f"Genes a Evaluar: {genes}\n"
        if adicionales:
            detalle += f"Genes Adicionales Solicitados: {adicionales}\n"
        if hallazgos:
            detalle += f"Se Solicitaron Hallazgos Secundarios \n"
        return detalle