from flask import Flask, render_template, Blueprint
from src.core.models.database import db
from src.core.models.usuario import Usuario
from src.core.models.rol import Rol  

bp = Blueprint('listar_usuarios', __name__)

@bp.route('/listar_usuarios')
def listar_usuarios():
    roles_permitidos = [2, 4, 6]
    usuarios = db.session.query(Usuario).join(Rol).filter(Usuario.id_rol.in_(roles_permitidos)).all()
    return render_template('owner/listar_usuarios.html', usuarios=usuarios)

