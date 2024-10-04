# Primeiro, importamos coisas mágicas que nos ajudam a guardar informações.
from adminflask import db, loginmanager
from datetime import datetime
from flask_login import UserMixin

@loginmanager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))

# Vamos criar um tipo de objeto chamado 'Usuario' para guardar informações dos usuários.
class Usuario(db.Model, UserMixin):
    # Damos um nome para nossa caixa de usuários.
    __tablename__ = 'usuarios'

    # Cada usuário tem um número especial para identificá-lo, chamado 'id'.
    id = db.Column(db.Integer, primary_key=True)

    # Cada usuário tem um nome.
    nome = db.Column(db.String(150), nullable=False)

    # Cada usuário tem um email único que ninguém mais pode ter.
    email = db.Column(db.String(150), unique=True, nullable=False)

    # Cada usuário tem uma senha secreta guardada de forma segura.
    senha = db.Column(db.String(256), nullable=False)

    foto_perfil = db.Column(db.String(150), nullable=True, default='default.png')  # Imagem de perfil
    is_active_user = db.Column(db.Boolean, default=True)
    def is_active(self):
        return self.is_active_user
    # Campo para verificar se o usuário é admin
    is_admin = db.Column(db.Boolean, default=False) 

    # Um usuário pode escrever muitos posts.
    posts = db.relationship('Post', backref='autor', lazy=True)

    # Um usuário pode ter muitos tokens para redefinir sua senha.
    tokens = db.relationship('TokenRedefinicao', backref='usuario', lazy=True)

class LogAcao(db.Model):
    __tablename__ = 'logs_acoes'
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)  # ID do usuário que realizou a ação
    entidade = db.Column(db.String(50), nullable=False)  # Tipo de entidade: 'post', 'usuario', etc.
    entidade_id = db.Column(db.Integer, nullable=True)  # ID da entidade que sofreu a ação (pode ser nulo)
    acao = db.Column(db.String(50), nullable=False)  # Tipo de ação: 'editar', 'excluir', 'criar', 'suspender'
    data_acao = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)  # Data e hora da ação
    descricao = db.Column(db.String(255), nullable=True)  # Descrição adicional da ação (opcional)

    def __repr__(self):
        return f'<LogAcao {self.id} - Usuário {self.usuario_id} - {self.acao} {self.entidade} {self.entidade_id}>'


class Mensagem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    conteudo = db.Column(db.Text, nullable=False)  # Conteúdo da mensagem
    data_envio = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)  # Data de envio
    remetente_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)  # ID de quem enviou (admin ou usuário)
    destinatario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)  # ID de quem recebeu a mensagem (admin ou usuário)
    sala = db.Column(db.String(100), nullable=False)  # Sala da mensagem, com base no ID do usuário ou 'admin'

    remetente = db.relationship('Usuario', foreign_keys=[remetente_id])  # Relacionamento com o usuário remetente
    destinatario = db.relationship('Usuario', foreign_keys=[destinatario_id])  # Relacionamento com o usuário destinatário


class Category(db.Model):
    __tablename__ = 'categories'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)  # Nome da categoria

    # Relacionamento com posts (assumindo que você tenha uma tabela de posts)
    posts = db.relationship('Post', backref='category', lazy=True)

    def __repr__(self):
        return f'<Category {self.name}>'

# Agora, vamos criar um tipo de objeto chamado 'Post' para guardar os posts que os usuários escrevem.
class Post(db.Model):
    # Damos um nome para nossa caixa de posts.
    __tablename__ = 'posts'

    # Cada post tem um número especial chamado 'id'.
    id = db.Column(db.Integer, primary_key=True)

    # Cada post tem um título.
    titulo = db.Column(db.String(200), nullable=False)

    # Cada post tem um conteúdo.
    conteudo = db.Column(db.Text, nullable=False)

    # Cada post sabe quando foi criado.
    data_criacao = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    # Cada post sabe quem o escreveu.
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)

    # ForeignKey: campo de categoria, referenciando o id da tabela Category
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)

# Vamos criar um tipo de objeto chamado 'TokenRedefinicao' para ajudar usuários a redefinir suas senhas.
class TokenRedefinicao(db.Model):
    # Damos um nome para nossa caixa de tokens.
    __tablename__ = 'tokens_redefinicao'

    # Cada token tem um número especial chamado 'id'.
    id = db.Column(db.Integer, primary_key=True)

    # O token é uma palavra secreta única.
    token = db.Column(db.String(100), nullable=False, unique=True)

    # O token sabe quando vai expirar.
    data_expiracao = db.Column(db.DateTime, nullable=False)

    # O token sabe de qual usuário ele é.
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)

# Agora, vamos criar um tipo de objeto chamado 'Curso' para guardar informações sobre cursos.
class Curso(db.Model):
    # Damos um nome para nossa caixa de cursos.
    __tablename__ = 'cursos'

    # Cada curso tem um número especial chamado 'id'.
    id = db.Column(db.Integer, primary_key=True)

    # Cada curso tem um nome.
    nome = db.Column(db.String(200), nullable=False)

    # Cada curso tem uma descrição.
    descricao = db.Column(db.Text, nullable=False)

    # Um curso pode ter muitos usuários inscritos.
    usuarios = db.relationship('Usuario', secondary='inscricoes', backref=db.backref('cursos', lazy='dynamic'))

# Criamos uma caixa especial chamada 'inscricoes' para ligar usuários e cursos.
inscricoes = db.Table('inscricoes',
    # Guarda o id do usuário que está inscrito.
    db.Column('usuario_id', db.Integer, db.ForeignKey('usuarios.id'), primary_key=True),
    # Guarda o id do curso em que o usuário está inscrito.
    db.Column('curso_id', db.Integer, db.ForeignKey('cursos.id'), primary_key=True)
)
