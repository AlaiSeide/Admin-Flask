from flask import Blueprint, render_template, url_for, redirect, flash, request
from flask_login import login_user, current_user, login_required, logout_user

from adminflask.forms import FormCriarConta, FormLogin
from adminflask.models import Usuario
from adminflask import db, bcrypt




main = Blueprint('main', __name__)

@main.route('/', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.homepage'))

    form = FormLogin()

    if form.validate_on_submit():
        usuario = Usuario.query.filter_by(email=form.email.data).first()
        if usuario and bcrypt.check_password_hash(usuario.senha, form.senha.data):
            login_user(usuario, remember=True)
            flash('Login feito com sucesso', 'alert-success')

            parametro_next = request.args.get('next')

            if parametro_next:
                return redirect(parametro_next)
            else:
                return redirect(url_for('main.homepage'))

        else:
            flash('Falha no Login email ou senha incoretos', 'alert-danger')
    return render_template('user/login.html', form=form)

@main.route('/criar_conta', methods=['GET', 'POST'])
def criar_conta():

    if current_user.is_authenticated:
        return redirect(url_for('main.homepage'))

    form = FormCriarConta()

    if form.validate_on_submit():

        senha_cript = bcrypt.generate_password_hash(form.senha.data)
        usuario = Usuario(nome=form.nome.data, email=form.email.data, senha=senha_cript)
        db.session.add(usuario)
        db.session.commit()
        flash('Conta Criada com Sucesso, faca Login', 'alert-success')
        return redirect(url_for('main.login'))
    return render_template('user/criar_conta.html', form=form)


@main.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logout feito com sucesso', 'alert-success')
    return redirect(url_for('main.homepage'))
    
@main.route('/termos-de-uso')
def termos_de_uso():
    return render_template('user/termos_de_uso.html')

@main.route('/politica-de-privacidade')
def politica_de_privacidade():
    return render_template('user/politica_de_privacidade.html')



@main.route('/homepage')
@login_required
def homepage():
    return render_template('user/homepage.html')
