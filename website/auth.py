import sqlite3
import bcrypt
from flask import Blueprint, render_template, request, flash, session, redirect, url_for
from dotenv import load_dotenv
from os import getenv, getcwd, path


auth = Blueprint('auth', __name__)
load_dotenv()


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        try:
            conn = sqlite3.connect(path.join(getcwd(), getenv('DB_NAME')))
            result = conn.cursor().execute("select email, password from users").fetchall()
            if len(result) > 0:
                if request.form.get('email') == result[0][0] and bcrypt.checkpw(request.form.get('password').encode(), result[0][1]):
                    session['email'] = request.form.get('email')
                    return redirect(url_for('views.home'))
                else:
                    flash("Kombinacja e-mailu i hasła nie jest poprawna.")
            else:
                flash("Na podany e-mail nie istnieje konto.")
            conn.close()
        except:
            flash("Podczas logowania wystąpił błąd.")
    return render_template("login.html")


@auth.route('/logout')
def logout():
    session.pop('email', None)
    return redirect(url_for('views.home'))


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        password_1 = request.form.get('password_1')
        password_2 = request.form.get('password_2')
        if password_1 != password_2:
            flash("Hasła są rózne.")
        if len(password_1) < 8:
            flash("Hasło musi mieć co najmniej 8 znaków.")
        else:
            try:
                conn = sqlite3.connect(path.join(getcwd(), getenv('DB_NAME')))
                if len(conn.cursor().execute(f"select email from users where email=?", (request.form.get('email'), )).fetchall()) > 0:
                    flash("Na podany e-mail istnieje już konto.")
                else:
                    hashed_password = bcrypt.hashpw(password_1.encode(), bcrypt.gensalt())
                    conn.cursor().execute("insert into users(email, password) values(?, ?)", (request.form.get('email'), hashed_password))
                    conn.commit()
                    session['email'] = request.form.get('email')
                    return redirect(url_for('views.home'))
                conn.close()
            except:
                flash("Podczas rejestracji wystąpił bład.")
    return render_template("sign-up.html")
