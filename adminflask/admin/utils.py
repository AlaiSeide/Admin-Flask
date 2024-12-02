from functools import wraps
from flask import abort
from flask_login import current_user, login_required
from werkzeug.utils import secure_filename
import os
from adminflask import app
import secrets
from adminflask import db
from adminflask.models import LogAcao


# Simplicidade nas rotas: Você só precisa usar @admin_required nas rotas de administrador.
# Consistência: Garante que todas as rotas que exigem acesso de administrador também verifiquem a autenticação.
# Decorator para verificar se o usuário é administrador e se esta autenticado
def admin_required(f):
    @wraps(f)
    @login_required  # Verifica se o usuário está autenticado
    def decorated_function(*args, **kwargs):
        if not current_user.is_admin:
            # Opcional: Você pode redirecionar ou mostrar uma mensagem personalizada
            abort(403)
        return f(*args, **kwargs)
    return decorated_function

def salvar_foto_perfil(foto):
    """Função para salvar a imagem de perfil com um nome único."""
    # Gera um nome de arquivo aleatório
    nome_aleatorio = secrets.token_hex(8)
    _ , extensao_arquivo = os.path.splitext(secure_filename(foto.filename))
    nome_arquivo = nome_aleatorio + extensao_arquivo

    caminho_foto = os.path.join(app.config['UPLOAD_FOLDER'], nome_arquivo)
    
    # Verifica se o diretório existe, caso contrário, cria o diretório
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    
    try:
        # Salva a imagem no caminho especificado
        foto.save(caminho_foto)
    except Exception as e:
        print(f"Erro ao salvar a imagem: {e}")
    return nome_arquivo

def registrar_log(usuario_id, entidade, entidade_id, acao, descricao=None):
    log = LogAcao(
        usuario_id=usuario_id,
        entidade=entidade,
        entidade_id=entidade_id,
        acao=acao,
        descricao=descricao
    )
    db.session.add(log)
    db.session.commit()
