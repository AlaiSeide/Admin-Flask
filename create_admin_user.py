from adminflask import db, bcrypt, app
from adminflask.models import Usuario

# Crie uma senha segura
senha_hash = bcrypt.generate_password_hash('Flashreverso2020..').decode('utf-8')

with app.app_context():
    # Crie o usuário administrador
    admin = Usuario(nome='Administrador', email='alaiseide2006@gmail.com', senha=senha_hash, is_admin=True)

    # Adicione o novo usuário no banco de dados
    db.session.add(admin)
    db.session.commit()