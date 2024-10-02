from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, EqualTo, Length, Email, ValidationError
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