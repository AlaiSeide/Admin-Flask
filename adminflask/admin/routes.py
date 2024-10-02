from flask import Blueprint, render_template, request, flash, redirect, url_for
from adminflask.models import Category, Usuario
from adminflask import db
admin = Blueprint('admin', __name__)






# Página de login para admin
@admin.route('/admin/', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Verifica se o usuário existe
        user = Usuario.query.filter_by(nome=username).first()

        if user and user.check_password(password) and user.is_admin:  # Verifica credenciais e se é admin
            session['user_id'] = user.id
            flash('Login efetuado com sucesso!', 'success')
            return redirect(url_for('admin.admin_dashboard'))
        else:
            flash('Credenciais inválidas ou acesso não autorizado.', 'danger')

    return render_template('admin/admin_login.html')




@admin.route('/admin/dashboard')
def admin_dashboard():
    return render_template('admin/dashboard.html')

@admin.route('/admin/users')
def admin_users():
    # Aqui você puxaria a lista de usuários do banco de dados
    users = []  # Exemplo
    return render_template('admin/users.html', users=users)

@admin.route('/admin/posts')
def admin_posts():
    # Aqui você puxaria a lista de posts do banco de dados
    posts = []  # Exemplo
    return render_template('admin/posts.html', posts=posts)


# Exibir página de gerenciamento de categorias
@admin.route('/admin/categories')
def admin_categories():
    categories = Category.query.all()  # Supondo que você tenha um modelo Category
    return render_template('admin/categories.html', categories=categories)

# Adicionar nova categoria
@admin.route('/admin/categories/add', methods=['POST'])
def add_category():
    category_name = request.form.get('category_name')
    if category_name:
        new_category = Category(name=category_name)
        db.session.add(new_category)
        db.session.commit()
        flash('Categoria adicionada com sucesso!', 'success')
    return redirect(url_for('admin.admin_categories'))

# Editar categoria
@admin.route('/admin/categories/<int:category_id>/edit', methods=['GET', 'POST'])
def edit_category(category_id):
    category = Category.query.get_or_404(category_id)
    if request.method == 'POST':
        category.name = request.form.get('category_name')
        db.session.commit()
        flash('Categoria atualizada com sucesso!', 'success')
        return redirect(url_for('admin.admin_categories'))
    return render_template('admin/edit_category.html', category=category)

# Excluir categoria
@admin.route('/admin/categories/<int:category_id>/delete')
def delete_category(category_id):
    category = Category.query.get_or_404(category_id)
    db.session.delete(category)
    db.session.commit()
    flash('Categoria excluída com sucesso!', 'success')
    return redirect(url_for('admin.admin_categories'))