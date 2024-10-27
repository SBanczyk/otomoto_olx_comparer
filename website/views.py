from flask import Blueprint, render_template


views = Blueprint('views', __name__)


@views.route('/')
def home():
    text = """<div class='d-flex justify-content-center align-items-center vh-100'>
                <h1>Prototyp aplikacji do porównywania ogłoszeń z serwisów OTOMOTO i OLX.</h1>
            </div>
            """
    return render_template("home.html", text=text)

