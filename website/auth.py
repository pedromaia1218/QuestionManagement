from flask import Blueprint, render_template

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    return render_template("login.html")

@auth.route('/logout')
def logout():
    return "Aqui vai ser feito o logout!"

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    return render_template("sign_up.html")