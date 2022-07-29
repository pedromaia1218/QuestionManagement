from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import Sector, User
from . import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        senha = request.form.get('senha')

        user = User.query.filter_by(email=email).first()
        if user:
            if senha == user.senha:
                flash('Logado com sucesso!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Senha errada.', category='error')
        else:
            flash('Email não cadastrado.', category='error')

    return render_template("login.html", user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/sign-up', methods=['GET', 'POST'])
@login_required
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        nome = request.form.get('nome')
        senha = request.form.get('senha')
        sector_id = request.form.get('setor')
        userType = request.form.get('userType')

        user = User.query.filter_by(email=email).first()
        

        if user:
            flash('Email já cadastrado!', category='error')
        elif len(nome) < 3:
            flash('Nome precisa ser maior que 2 caracteres.', category='error')
        else:
            new_user = User(email=email, nome=nome, senha=senha, sector_id=sector_id, userType=userType)
            db.session.add(new_user)
            db.session.commit()

            flash('Conta criada com sucesso!', category='success')
            return redirect(url_for('views.home'))

    if(current_user.userType == 'admin'):
        sector = Sector.query.all()
        return render_template("sign_up.html", user=current_user, sector=sector)
    else:
        flash('Não permitido.', category='error')
        return redirect(url_for('views.home'))