from flask import Blueprint, render_template, request, flash, redirect, url_for, flash
from flask_login import login_required, current_user, login_user, logout_user
from adminflask.forms import AdminLogin
from adminflask.models import Category, Usuario
from adminflask import db, bcrypt, loginmanager
from adminflask.admin.utils import admin_required
admin = Blueprint('admin', __name__)


# Página de login para admin
@admin.route('/', methods=['GET', 'POST'])
def admin_login():
    if current_user.is_authenticated and current_user.is_admin:
        return redirect(url_for('admin.admin_dashboard'))

    form = AdminLogin()
    if form.validate_on_submit():
        user = Usuario.query.filter_by(email=form.email.data).first()

        # Verifica se as credenciais são corretas e se o usuário é admin
        if user and bcrypt.check_password_hash(user.senha, form.senha.data) and user.is_admin:
            login_user(user)
            flash('Login efetuado com sucesso!', 'alert-success')

            # Redireciona para a página desejada (next_admin) ou para o dashboard do admin
            next_admin = request.args.get('next_admin')  # Campo para redirecionamento de admin
            return redirect(next_admin) if next_admin else redirect(url_for('admin.admin_dashboard'))
        else:
            flash('Credenciais inválidas ou acesso não autorizado.', 'alert-danger')

    return render_template('admin/admin_login.html', form=form)


@admin.route('/logout')
@login_required
@admin_required
def admin_logout():
    logout_user()
    flash('Logout feito com sucesso', 'alert-success')
    return redirect(url_for('admin.admin_login'))

@admin.route('/dashboard')
@login_required
@admin_required
def admin_dashboard():
    return render_template('admin/dashboard.html')

@admin.route('/users')
@login_required
@admin_required
def admin_users():
    # Aqui você puxaria a lista de usuários do banco de dados
    users = Usuario.query.all()
    return render_template('admin/users.html', users=users)

@admin.route('/posts')
@login_required
@admin_required
def admin_posts():
    # Aqui você puxaria a lista de posts do banco de dados
    posts = []  # Exemplo
    return render_template('admin/posts.html', posts=posts)


# Exibir página de gerenciamento de categorias
@admin.route('/categories')
@login_required
@admin_required
def admin_categories():
    categories = Category.query.all()  # Supondo que você tenha um modelo Category
    return render_template('admin/categories.html', categories=categories)

# Adicionar nova categoria
@admin.route('/categories/add', methods=['POST'])
@login_required
@admin_required
def add_category():
    category_name = request.form.get('category_name')
    if category_name:
        new_category = Category(name=category_name)
        db.session.add(new_category)
        db.session.commit()
        flash('Categoria adicionada com sucesso!', 'success')
    return redirect(url_for('admin.admin_categories'))

# Editar categoria
@admin.route('/categories/<int:category_id>/edit', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_category(category_id):
    category = Category.query.get_or_404(category_id)
    if request.method == 'POST':
        category.name = request.form.get('category_name')
        db.session.commit()
        flash('Categoria atualizada com sucesso!', 'success')
        return redirect(url_for('admin.admin_categories'))
    return render_template('admin/edit_category.html', category=category)

# Excluir categoria
@admin.route('/categories/<int:category_id>/delete')
@login_required
@admin_required
def delete_category(category_id):
    category = Category.query.get_or_404(category_id)
    db.session.delete(category)
    db.session.commit()
    flash('Categoria excluída com sucesso!', 'success')
    return redirect(url_for('admin.admin_categories'))