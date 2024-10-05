from flask import Flask, request, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, current_user, logout_user
from flask_migrate import Migrate
import os

server = '192.168.178.4'

app = Flask(__name__)
# pip install mysql-connector-python
# para se conectar ao banco mysql remotamente precisamos dessa biblioteca encima.
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+mysqlconnector://alaiseide:2040Amor..@{server}/Admin'
app.config['SECRET_KEY'] = '840966b21520d9cc13a2df0ae47f4bec'
# Diretório onde as fotos de perfil serão armazenadas
app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'static', 'images', 'perfis')
# app.config['UPLOAD_FOLDER'] = 'static/images'

db = SQLAlchemy(app)
migrate = Migrate(app, db)
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


# Usando o @before_request, você garante que os usuários suspensos sejam imediatamente desconectados ao tentar acessar qualquer parte do sistema. Dessa forma, a suspensão é aplicada de forma imediata e eficaz.
# Função que verifica o status do usuário em cada requisição
@app.before_request
def verificar_status_usuario():
    # Verifica se o usuário está autenticado
    if current_user.is_authenticated:
        # Verifica se o usuário está suspenso (is_active_user == False)
        if not current_user.is_active_user:
            # Desconecta o usuário suspenso
            logout_user()
            # Exibe uma mensagem de conta suspensa
            flash('Sua conta está suspensa. Entre em contato com o administrador.', 'alert-danger')
            # Redireciona o usuário para a página de login
            return redirect(url_for('main.login'))

# Registrar as blueprints
from adminflask.main.routes import main
from adminflask.admin.routes import admin
from adminflask.post.routes import post

app.register_blueprint(main)
app.register_blueprint(admin, url_prefix='/admin')  # Prefixo para rotas administrativas
app.register_blueprint(post)
