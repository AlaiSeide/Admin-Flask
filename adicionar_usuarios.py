from adminflask import db, bcrypt, app
from adminflask.models import Usuario

def adicionar_usuarios_teste(quantidade):
    for i in range(1, quantidade + 1):
        nome = f'Usuário {i}'
        email = f'usuario{i}@exemplo.com'
        senha_hash = bcrypt.generate_password_hash('senha123').decode('utf-8')
        usuario = Usuario(
            nome=nome,
            email=email,
            senha=senha_hash,
            is_active_user=True
        )
        db.session.add(usuario)
    db.session.commit()
    print(f'{quantidade} usuários adicionados com sucesso!')

if __name__ == '__main__':
    # Ativa o contexto da aplicação
    with app.app_context():
        adicionar_usuarios_teste(quantidade=25)
