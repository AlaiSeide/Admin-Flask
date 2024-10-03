from flask import Blueprint, render_template, url_for, redirect, flash, request
from flask_login import login_user, current_user, login_required, logout_user

from adminflask.forms import FormCriarConta, FormLogin, PostForm
from adminflask.models import Usuario, Curso, Post
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
    curso = Curso.query.all()
    return render_template('user/homepage.html', cursos=curso)

@main.route('/posts/')
@login_required
def ver_post(post_id):
    post = Post.query.all()
    return render_template('user/ver_post.html', post=post)

@main.route('/posts/adicionar', methods=['GET', 'POST'])
@login_required
def adicionar_post():
    form = PostForm()
    if form.validate_on_submit():
        # Cria um novo post com os dados do formulário e o usuário logado como autor
        novo_post = Post(titulo=form.titulo.data, conteudo=form.conteudo.data, usuario_id=current_user.id, category_id=form.category.data)
        db.session.add(novo_post)
        db.session.commit()
        flash('Seu post foi criado com sucesso!', 'alert-success')
        return redirect(url_for('main.ver_post', post_id=novo_post.id))
    
    return render_template('user/adicionar_post.html', form=form)

@main.route('/posts/<int:post_id>/editar', methods=['GET', 'POST'])
@login_required
def editar_post(post_id):
    post = Post.query.get_or_404(post_id)
    
    # Verifica se o usuário logado é o autor do post
    if post.usuario_id != current_user.id:
        flash('Você não tem permissão para editar este post.', 'alert-danger')
        return redirect(url_for('main.ver_post', post_id=post.id))
    
    form = PostForm()
    if form.validate_on_submit():
        post.titulo = form.titulo.data
        post.conteudo = form.conteudo.data
        post.category_id = form.category.data
        db.session.commit()
        flash('Seu post foi atualizado com sucesso!', 'alert-success')
        return redirect(url_for('main.ver_post', post_id=post.id))
    
    form.titulo.data = post.titulo
    form.conteudo.data = post.conteudo
    form.category.data = post.category_id
    return render_template('user/editar_post.html', form=form, post=post)

@main.route('/posts/<int:post_id>/excluir', methods=['POST'])
@login_required
def excluir_post(post_id):
    post = Post.query.get_or_404(post_id)
    
    # Verifica se o usuário logado é o autor do post
    if post.usuario_id != current_user.id:
        flash('Você não tem permissão para excluir este post.', 'alert-danger')
        return redirect(url_for('main.ver_post', post_id=post.id))
    
    db.session.delete(post)
    db.session.commit()
    flash('Seu post foi excluído com sucesso!', 'alert-success')
    return redirect(url_for('main.homepage'))


# cursos
@main.route('/cursos')
@login_required
def ver_cursos():
    cursos = Curso.query.all()  # Pega todos os cursos do banco de dados
    return render_template('user/ver_cursos.html', cursos=cursos)

@main.route('/cursos/<int:curso_id>/inscrever')
@login_required
def inscrever_curso(curso_id):
    curso = Curso.query.get_or_404(curso_id)
    if current_user not in curso.usuarios:
        curso.usuarios.append(current_user)
        db.session.commit()
        flash(f'Você foi inscrito no curso "{curso.nome}"!', 'alert-success')
    else:
        flash(f'Você já está inscrito no curso "{curso.nome}".', 'alert-info')
    return redirect(url_for('main.ver_curso', curso_id=curso.id))
