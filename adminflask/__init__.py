from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, current_user
import os

server = '192.168.178.4'

app = Flask(__name__)
# pip install mysql-connector-python
# para se conectar ao banco mysql remotamente precisamos dessa biblioteca encima.
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+mysqlconnector://alaiseide:2040Amor..@{server}/Admin'
app.config['SECRET_KEY'] = '840966b21520d9cc13a2df0ae47f4bec'
app.config['UPLOAD_FOLDER'] = 'static/images'

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
loginmanager = LoginManager(app)
loginmanager.login_message = 'Faça login para acessar esta página, por favor'
loginmanager.login_message_category = 'alert-info'

#Se o usuário não estiver autenticado e estiver tentando acessar a área de admin, o login_manager.login_view é configurado para admin.admin_login, redirecionando para a página de login de administradores.
#Caso contrário, o login_manager.login_view é configurado de volta para o login de usuários normais (usuarios.login).

# Função para redirecionar para o login de admin, se necessário

# Verificação de login para admin e usuários normais
@app.before_request
def verificar_login():
    # Verifica se o usuário não está autenticado
    if not current_user.is_authenticated:
        # Se a rota pertence ao admin, redireciona para o login de admin
        if request.endpoint and request.endpoint.startswith('admin.'):
            loginmanager.login_view = 'admin.admin_login'
        else:
            # Senão, redireciona para o login de usuários normais
            loginmanager.login_view = 'main.login'


# Registrar as blueprints
from adminflask.main.routes import main
from adminflask.admin.routes import admin
from adminflask.post.routes import post

app.register_blueprint(main)
app.register_blueprint(admin, url_prefix='/admin')  # Prefixo para rotas administrativas
app.register_blueprint(post)
