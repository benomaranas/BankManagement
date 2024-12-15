from flask import Flask
from app.controller import app_routes
def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your_secret_key'
    
    with app.app_context():
        from app import controller
        app.register_blueprint(app_routes)
    return app