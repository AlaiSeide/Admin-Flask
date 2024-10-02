from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
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
loginmanager.login_view = 'main.login'
loginmanager.login_message = 'Faca login para acessar esta pagina, por favor'
loginmanager.login_message_category = 'alert-info'


# Registrar as blueprints
from adminflask.main.routes import main
from adminflask.admin.routes import admin
from adminflask.post.routes import post

app.register_blueprint(main)
app.register_blueprint(admin)
app.register_blueprint(post)

