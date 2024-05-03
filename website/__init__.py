from flask import Flask
from .views import views
from .models import models

def create_app():
    app = Flask(__name__)
    app.secret_key = 'TEST'

    app.register_blueprint(views)
    app.register_blueprint(models)

    return app
