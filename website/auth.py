from flask import Blueprint, render_template, request, flash, session, redirect, url_for
from dotenv import load_dotenv
from os import getenv, getcwd, path
import sqlite3


auth = Blueprint('auth', __name__)
load_dotenv()


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        db_path = path.join(getcwd(), getenv('DB_NAME'))
        conn = sqlite3.connect(db_path)
        result = conn.cursor().execute("select email, password from users").fetchall()
        if request.form.get('email') == result[0][0] and request.form.get('password') == result[0][1]:
            session['email'] = request.form.get('email')
            return redirect(url_for('views.home'))
        else:
            flash("NOT OK", category="error")
        conn.close()
    return render_template("login.html")


@auth.route('/logout')
def logout():
    session.pop('email', None)
    return redirect(url_for('views.home'))


@auth.route('/sign-up')
def sign_up():
    text = """<div class='d-flex justify-content-center align-items-center vh-100' style='max-height: 90vh'>
                <h1>Rejestracja.</h1>
            </div>
            """
    return render_template("sign-up.html", text=text)
