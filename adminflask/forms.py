from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, SelectField
from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import DataRequired, EqualTo, Length, Email, ValidationError, Optional
from adminflask.models import Usuario

class FormCriarConta(FlaskForm):
    nome = StringField('Nome Completo', validators=[DataRequired()])
    email = StringField('Endereço de Email', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired(), Length(6, 20)])
    confirmacao_senha = PasswordField('Confirme a Senha', validators=[DataRequired(), EqualTo('senha')])
    botao_criar_conta = SubmitField('Criar Conta')

    def validate_email(self, email):
        usuario = Usuario.query.filter_by(email=email.data).first()
        if usuario:
            raise ValidationError('E-mail ja cadastrado. Cadastre-se com outro e-mail ou faca login para continuar')

class FormLogin(FlaskForm):
    email = StringField('Endereço de Email', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired(), Length(6, 20)])
    botao_fazer_login = SubmitField('Login')


class AdminLogin(FlaskForm):
    email = StringField('Endereço de Email', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired(), Length(6, 20)])
    botao_fazer_login = SubmitField('Login')


class EditUserForm(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    is_admin = BooleanField('É administrador?')
    senha = PasswordField('Senha (somente para mudar sua própria senha)', validators=[Optional()])  # Campo opcional para editar senha
    submit = SubmitField('Atualizar')

class ConfirmDeleteForm(FlaskForm):
    confirmar = BooleanField('Você tem certeza que deseja excluir este usuário?', validators=[DataRequired()])
    submit = SubmitField('Excluir')   

class CreateUserForm(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired(), Length(min=2, max=150)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired(), Length(min=6)])
    is_admin = BooleanField('Administrador?')
    submit = SubmitField('Criar Usuário')   

class AdminProfileForm(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired(), Length(min=2, max=150)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    senha = PasswordField('Nova Senha (opcional)', validators=[Optional(), Length(min=6)])
    foto_perfil = FileField('Atualizar Foto de Perfil', validators=[Optional(), FileAllowed(['jpg', 'png'], 'Apenas imagens JPG ou PNG!')])
    submit = SubmitField('Atualizar Perfil')

class CursoForm(FlaskForm):
    nome = StringField('Nome do Curso', validators=[DataRequired(), Length(min=5, max=200)])
    descricao = TextAreaField('Descrição', validators=[DataRequired(), Length(min=10)])
    submit = SubmitField('Cadastrar Curso')

class PostForm(FlaskForm):
    titulo = StringField('Título', validators=[DataRequired(), Length(min=5, max=200)])
    conteudo = TextAreaField('Conteúdo', validators=[DataRequired()])
    category = SelectField('Categoria', coerce=int)  # Vamos preencher as opções no back-end
    submit = SubmitField('Salvar Post')