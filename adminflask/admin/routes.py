from flask import Blueprint, render_template, request, flash, redirect, url_for, flash
from flask_login import login_required, current_user, login_user, logout_user
from adminflask.forms import AdminLogin, EditUserForm, ConfirmDeleteForm, CreateUserForm, AdminProfileForm, CursoForm
from adminflask.models import Category, Usuario, Curso
from adminflask import db, bcrypt, loginmanager
from adminflask.admin.utils import admin_required, salvar_foto_perfil
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
@admin_required
def admin_logout():
    logout_user()
    flash('Logout feito com sucesso', 'alert-success')
    return redirect(url_for('admin.admin_login'))


@admin.route('/dashboard')
@admin_required
def admin_dashboard():
    return render_template('admin/dashboard.html')

@admin.route('/profile', methods=['GET', 'POST'])
@admin_required
def admin_profile():
    form = AdminProfileForm()

    if form.validate_on_submit():
        # Atualiza o nome e e-mail do administrador
        current_user.nome = form.nome.data
        current_user.email = form.email.data

        # Se o administrador quiser alterar a senha
        if form.senha.data:
            senha_hash = bcrypt.generate_password_hash(form.senha.data).decode('utf-8')
            current_user.senha = senha_hash
            flash('Sua senha foi alterada com sucesso.', 'alert-success')

        # Se o administrador quiser alterar a foto de perfil
        if form.foto_perfil.data:
            foto_arquivo = salvar_foto_perfil(form.foto_perfil.data)
            current_user.foto_perfil = foto_arquivo  # Salva o nome da foto no banco de dados

        # Salva as alterações no banco de dados
        db.session.commit()
        flash('Seu perfil foi atualizado com sucesso.', 'alert-success')
        return redirect(url_for('admin.admin_profile'))

    # Preenche os campos do formulário com os dados atuais do usuário
    form.nome.data = current_user.nome
    form.email.data = current_user.email

    return render_template('admin/profile.html', form=form)

# Associa a rota '/users' ao blueprint 'admin'
@admin.route('/users')
# Aplica o decorador 'admin_required' para garantir que apenas administradores possam acessar a rota
@admin_required
def admin_users():
    # Obtém o parâmetro 'search' da URL (por exemplo, '/users?search=nome'), ou usa uma string vazia se não estiver presente
    search_query = request.args.get('search', '', type=str)
    # Obtém o parâmetro 'page' da URL para paginação (por exemplo, '/users?page=2'), ou usa 1 se não estiver presente
    page = request.args.get('page', 1, type=int)

    # Verifica se há uma consulta de busca (se o usuário digitou algo no campo de busca)
    if search_query:
        # Realiza uma consulta no banco de dados filtrando usuários cujo nome ou email contém a string de busca, ignorando maiúsculas e minúsculas
        users = Usuario.query.filter(
            # Filtra pelo nome usando 'ilike' para uma comparação insensível a maiúsculas/minúsculas
            Usuario.nome.ilike(f'%{search_query}%') |
            # Filtra pelo email da mesma forma
            Usuario.email.ilike(f'%{search_query}%')
        ).paginate(page=page, per_page=10)  # Divide os resultados em páginas de 10 itens
    else:
        # Se não houver busca, obtém todos os usuários com paginação
        users = Usuario.query.paginate(page=page, per_page=10)

    # Renderiza o template 'admin/users.html', passando a lista de usuários e a consulta de busca atual
    return render_template('admin/users.html', users=users, search_query=search_query)

@admin.route('/users/<int:user_id>/toggle_active')
@admin_required
def toggle_user_active(user_id):
    user = Usuario.query.get_or_404(user_id)
    user.is_active_user = not user.is_active_user
    db.session.commit()
    status = 'ativado' if user.is_active_user else 'suspenso'
    flash(f'Usuário {user.nome} foi {status} com sucesso.', 'success')
    return redirect(url_for('admin.admin_users'))


@admin.route('/users/new', methods=['GET', 'POST'])
@admin_required
def create_user():
    form = CreateUserForm()
    
    if form.validate_on_submit():
        # Cria uma senha criptografada
        senha_hash = bcrypt.generate_password_hash(form.senha.data).decode('utf-8')
        # Cria o novo usuário
        novo_usuario = Usuario(nome=form.nome.data, email=form.email.data, senha=senha_hash, is_admin=form.is_admin.data)
        # Salva o usuário no banco de dados
        db.session.add(novo_usuario)
        db.session.commit()
        
        flash(f'Novo usuário {novo_usuario.nome} foi criado com sucesso.', 'alert-success')
        return redirect(url_for('admin.admin_users'))

    return render_template('admin/create_user.html', form=form)

@admin.route('/users/<int:user_id>')
@admin_required
def view_user(user_id):
    user = Usuario.query.get_or_404(user_id)
    return render_template('admin/view_user.html', user=user)


@admin.route('/users/<int:user_id>/edit', methods=['GET', 'POST'])
@admin_required
def edit_user(user_id):
    user = Usuario.query.get_or_404(user_id)
    form = EditUserForm()

    if form.validate_on_submit():
        # Atualiza os campos nome, email, e status de admin
        user.nome = form.nome.data
        user.email = form.email.data
        user.is_admin = form.is_admin.data

        # Verifica se o admin está editando sua própria conta e se quer mudar a senha
        if user.id == current_user.id and form.senha.data:
            senha_hash = bcrypt.generate_password_hash(form.senha.data).decode('utf-8')
            user.senha = senha_hash
            flash('Sua senha foi alterada com sucesso.', 'alert-success')

        db.session.commit()
        flash('As informações do usuário foram atualizadas com sucesso.', 'alert-success')
        return redirect(url_for('admin.admin_users'))

    # Preenche o formulário com os dados atuais do usuário
    form.nome.data = user.nome
    form.email.data = user.email
    form.is_admin.data = user.is_admin

    # Se o administrador estiver editando outro usuário, mostra um campo de senha "não editável"
    if user.id != current_user.id:
       form.senha.render_kw = {
           'disabled': True,  # Desativa o campo para outros usuários
            'type': 'password',  # Define como tipo password para mostrar pontinhos
            'placeholder': '••••••••••'
        }# Exibe senha com pontinhos e torna o campo não editável

    return render_template('admin/edit_user.html', form=form, user=user)

@admin.route('/users/<int:user_id>/delete', methods=['GET', 'POST'])
@admin_required  # Certifique-se de que apenas admin pode acessar
def delete_user(user_id):
    user = Usuario.query.get_or_404(user_id)
    form = ConfirmDeleteForm()

    # Verifica se o administrador está tentando excluir a si mesmo (opcional)
    if user.id == current_user.id:
        flash('Você não pode excluir a sua própria conta.', 'alert-danger')
        return redirect(url_for('admin.admin_users'))

    if form.validate_on_submit() and form.confirmar.data:
        # Excluir os dados associados ao usuário (exemplo: posts)
        for post in user.posts:
            db.session.delete(post)

        # Excluir o próprio usuário
        db.session.delete(user)
        db.session.commit()

        flash(f'Usuário {user.nome} foi excluído com sucesso.', 'alert-success')
        return redirect(url_for('admin.admin_users'))

    return render_template('admin/delete_user.html', form=form, user=user)


# posts
@admin.route('/posts')
@admin_required
def admin_posts():
    # Aqui você puxaria a lista de posts do banco de dados
    posts = []  # Exemplo
    return render_template('admin/posts.html', posts=posts)


# Exibir página de gerenciamento de categorias
@admin.route('/categories')
@admin_required
def admin_categories():
    categories = Category.query.all()  # Supondo que você tenha um modelo Category
    return render_template('admin/categories.html', categories=categories)

# Adicionar nova categoria
@admin.route('/categories/add', methods=['POST'])
@admin_required
def add_category():
    category_name = request.form.get('category_name')
    if category_name:
        new_category = Category(name=category_name)
        db.session.add(new_category)
        db.session.commit()
        flash('Categoria adicionada com sucesso!', 'alert-success')
    return redirect(url_for('admin.admin_categories'))

# Editar categoria
@admin.route('/categories/<int:category_id>/edit', methods=['GET', 'POST'])
@admin_required
def edit_category(category_id):
    category = Category.query.get_or_404(category_id)
    if request.method == 'POST':
        category.name = request.form.get('category_name')
        db.session.commit()
        flash('Categoria atualizada com sucesso!', 'alert-success')
        return redirect(url_for('admin.admin_categories'))
    return render_template('admin/edit_category.html', category=category)

# Excluir categoria
@admin.route('/categories/<int:category_id>/delete')
@admin_required
def delete_category(category_id):
    category = Category.query.get_or_404(category_id)
    db.session.delete(category)
    db.session.commit()
    flash('Categoria excluída com sucesso!', 'alert-success')
    return redirect(url_for('admin.admin_categories'))

# cursos

@admin.route('/cursos')
@admin_required
def admin_cursos():
    # Busca todos os cursos cadastrados
    cursos = Curso.query.all()
    return render_template('admin/cursos.html', cursos=cursos)

@admin.route('/cursos/cadastrar', methods=['GET', 'POST'])
@admin_required
def admin_cadastrar_curso():
    form = CursoForm()
    if form.validate_on_submit():
        # Cria um novo curso com os dados do formulário
        novo_curso = Curso(nome=form.nome.data, descricao=form.descricao.data)
        db.session.add(novo_curso)  # Adiciona o curso no banco de dados
        db.session.commit()  # Salva a transação
        flash(f'Curso "{novo_curso.nome}" cadastrado com sucesso!', 'alert-success')
        return redirect(url_for('admin.admin_dashboard'))  # Redireciona para o dashboard ou outra página
    return render_template('admin/cadastrar_curso.html', form=form)

@admin.route('/cursos/<int:curso_id>/editar', methods=['GET', 'POST'])
@admin_required
def editar_curso(curso_id):
    curso = Curso.query.get_or_404(curso_id)
    form = CursoForm()

    if form.validate_on_submit():
        curso.nome = form.nome.data
        curso.descricao = form.descricao.data
        db.session.commit()
        flash(f'Curso "{curso.nome}" atualizado com sucesso.', 'alert-success')
        return redirect(url_for('admin.admin_cursos'))

    form.nome.data = curso.nome
    form.descricao.data = curso.descricao
    return render_template('admin/editar_curso.html', form=form, curso=curso)

@admin.route('/cursos/<int:curso_id>/deletar', methods=['POST'])
@admin_required
def deletar_curso(curso_id):
    curso = Curso.query.get_or_404(curso_id)
    db.session.delete(curso)
    db.session.commit()
    flash(f'Curso "{curso.nome}" excluído com sucesso.', 'alert-success')
    return redirect(url_for('admin.admin_cursos'))

