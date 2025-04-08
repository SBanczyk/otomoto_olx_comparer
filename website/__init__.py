import os
from flask import Flask
from .views import views
from .auth import auth
from .comp import comp


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(comp, url_prefix='/')
    return app
