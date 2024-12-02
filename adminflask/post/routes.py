from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from adminflask.models import Post, Category
from adminflask.forms import PostForm
from adminflask import db
post = Blueprint('post', __name__)


@post.route('/posts')
@login_required
def ver_posts():
    # Busca todos os posts do banco de dados
    posts = Post.query.all()
    # Passa os posts para o template
    return render_template('post/ver_posts.html', posts=posts)


@post.route('/posts/adicionar', methods=['GET', 'POST'])
@login_required
def adicionar_post():
    form = PostForm()

    # Buscar todas as categorias do banco de dados e preencher o campo 'category' no formulário
    form.category.choices = [(categoria.id, categoria.name) for categoria in Category.query.all()]

    if form.validate_on_submit():
        # Cria um novo post com os dados do formulário e o usuário logado como autor
        novo_post = Post(titulo=form.titulo.data,
            conteudo=form.conteudo.data,
            usuario_id=current_user.id,
            category_id=form.category.data
            )
        db.session.add(novo_post)
        db.session.commit()
        flash('Seu post foi criado com sucesso!', 'alert-success')
        return redirect(url_for('post.detalhes_post', post_id=novo_post.id))
    
    return render_template('post/adicionar_post.html', form=form)

@post.route('/posts/<int:post_id>/editar', methods=['GET', 'POST'])
@login_required
def editar_post(post_id):
    post = Post.query.get_or_404(post_id)
    
    
    # Verifica se o usuário logado é o autor do post
    if post.usuario_id != current_user.id:
        flash('Você não tem permissão para editar este post.', 'alert-danger')
        return redirect(url_for('post.detalhes_post', post_id=post.id))
    
    form = PostForm()

    # Buscar todas as categorias do banco de dados e preencher o campo 'category' no formulário
    form.category.choices = [(categoria.id, categoria.name) for categoria in Category.query.all()]
    
    if form.validate_on_submit():
        post.titulo = form.titulo.data
        post.conteudo = form.conteudo.data
        post.category_id = form.category.data
        db.session.commit()
        flash('Seu post foi atualizado com sucesso!', 'alert-success')
        return redirect(url_for('post.detalhes_post', post_id=post.id))
    
    form.titulo.data = post.titulo
    form.conteudo.data = post.conteudo
    form.category.data = post.category_id
    return render_template('post/editar_post.html', form=form, post=post)

@post.route('/post/<int:post_id>')
@login_required
def detalhes_post(post_id):
    post = Post.query.get_or_404(post_id)  # Busca o post no banco de dados
    return render_template('post/detalhes_post.html', post=post)


@post.route('/posts/<int:post_id>/excluir', methods=['POST'])
@login_required
def excluir_post(post_id):
    post = Post.query.get_or_404(post_id)
    
    # Verifica se o usuário logado é o autor do post
    if post.usuario_id != current_user.id:
        flash('Você não tem permissão para excluir este post.', 'alert-danger')
        return redirect(url_for('post.detalhes_post', post_id=post.id))
    
    db.session.delete(post)
    db.session.commit()
    flash('Seu post foi excluído com sucesso!', 'alert-success')
    return redirect(url_for('main.homepage'))
