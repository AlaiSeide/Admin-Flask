from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

server = '192.168.178.4'

app = Flask(__name__)
# pip install mysql-connector-python
# para se conectar ao banco mysql remotamente precisamos dessa biblioteca encima.
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+mysqlconnector://alaiseide:2040Amor..@{server}/Admin'
app.config['SECRET_KEY'] = '9b4f2d8050ae28c1b0354f4bd7aa8e62'
app.config['UPLOAD_FOLDER'] = 'static/images'
db = SQLAlchemy(app)

# Registrar as blueprints
from adminflask.main.routes import main
from adminflask.admin.routes import admin
from adminflask.post.routes import post

app.register_blueprint(main)
app.register_blueprint(admin)
app.register_blueprint(post)

