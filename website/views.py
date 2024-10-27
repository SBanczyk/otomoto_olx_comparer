from flask import Blueprint, render_template


views = Blueprint('views', __name__)


@views.route('/')
def home():
    text = """<div class='d-flex justify-content-center align-items-center vh-100' style='max-height: 90vh'>
                <h3>Prototyp aplikacji do porównywania ogłoszeń z serwisów OTOMOTO i OLX.</h3>
            </div>
            """
    return render_template("home.html", text=text)

