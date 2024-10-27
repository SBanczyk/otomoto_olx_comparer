from flask import Blueprint, render_template


auth = Blueprint('auth', __name__)


@auth.route('/login')
def login():
    text = """<div class='d-flex justify-content-center align-items-center vh-100'>
                <h1>Logowanie.</h1>
            </div>
            """
    return render_template("login.html", text=text)


@auth.route('/logout')
def logout():
    text = """<div class='d-flex justify-content-center align-items-center vh-100'>
                <h1>Wylogowanie.</h1>
            </div>
            """
    return render_template("logout.html", text=text)


@auth.route('/sign-up')
def sign_up():
    text = """<div class='d-flex justify-content-center align-items-center vh-100'>
                <h1>Rejestracja.</h1>
            </div>
            """
    return render_template("sign-up.html", text=text)