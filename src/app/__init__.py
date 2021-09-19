from flask_ngrok import run_with_ngrok
from flask_bootstrap import Bootstrap
from .views import notion_admin
from flask import Flask

def create_app():

    app = Flask(__name__)
    run_with_ngrok(app)   #starts ngrok when the app is run
    app.config['SECRET_KEY'] = "some_super_secret_key"
    bootstrap = Bootstrap(app)
    
    app.register_blueprint(notion_admin)


    return app

