from adminflask.models import *
from adminflask import db, app

with app.app_context():
    db.create_all()

