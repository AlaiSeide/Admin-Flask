from functools import wraps
from flask import abort
from flask_login import current_user

# Decorator para verificar se o usuário é administrador
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            # Se o usuário não estiver autenticado, retorna erro 403 (acesso proibido)
            abort(403)
        if not current_user.is_admin:
            # Se o usuário não for administrador, retorna erro 403 (acesso proibido)
            abort(403)
        return f(*args, **kwargs)
    return decorated_function
