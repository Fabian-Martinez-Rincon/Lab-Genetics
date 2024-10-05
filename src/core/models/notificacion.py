from src.core.models.database import db
from src.core.models.usuario import Usuario
from flask_mail import Mail, Message
from flask import current_app

class Notificacion(db.Model):
    __tablename__="notificaciones"
    id = db.Column(db.Integer, primary_key=True, unique= True)
    descripcion = db.Column(db.String(255), nullable=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey("usuarios.id"), nullable=False)

    @staticmethod
    def send_mail(userId: int, descripcion: str)->None:
        """
        Send the confirmation email to the user.
        """
        app = current_app._get_current_object()
        usuario = Usuario.query.filter_by(id=userId).first()
        mail = Mail(app)
        subject = 'Nueva Notificacion'
        sender = app.config['MAIL_DEFAULT_SENDER']
        recipients = [usuario.email]
        message = f'¡Atencion! Se le notifica que:\n{descripcion}\n\n Para Conocer mas detalles ingrese a la plataforma.'
        msg = Message(subject, sender=sender, recipients=recipients)
        msg.body = message
        mail.send(msg)       
        
    @staticmethod
    def send_mail2(email: str, descripcion: str)->None:
        """
        Send the confirmation email to the user.
        """
        app = current_app._get_current_object()
        mail = Mail(app)
        subject = 'Nueva Notificacion'
        sender = app.config['MAIL_DEFAULT_SENDER']
        recipients = [email]
        message = f'¡Atencion! Se le notifica que:\n{descripcion}'
        msg = Message(subject, sender=sender, recipients=recipients)
        msg.body = message
        mail.send(msg)

    @classmethod
    def informarPenalizacion(self, id_usuario: int, motivo: str) -> None:
        """
        Envia una notificacion y un correo electronico al usuario cuando recibe una penalizacion
        """
        usuario = Usuario.query.filter_by(id=id_usuario).first()
        descripcion = f"Has recibido una penalización. Motivo: {motivo}"
        new_notificacion = Notificacion(id_usuario=id_usuario, descripcion=descripcion)
        self.send_mail(id_usuario, descripcion)
        db.session.add(new_notificacion)
        db.session.commit()
    
    @classmethod
    def informarEliminacionUsuario(self, id_usuario: int, motivo: str) -> None:
        """
        Envía una notificación y un correo electrónico al usuario cuando es eliminado.
        """
        usuario = Usuario.query.filter_by(id=id_usuario).first()
        descripcion = f"Tu cuenta ha sido eliminada. Motivo: {motivo}"
        new_notificacion = Notificacion(id_usuario=id_usuario, descripcion=descripcion)
        self.send_mail(id_usuario, descripcion)
        db.session.add(new_notificacion)
        db.session.commit()