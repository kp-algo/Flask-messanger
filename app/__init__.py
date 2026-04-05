from flask import Flask
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy 
from flask_login import LoginManager
from config import Config

# 1. Initialize extensions (Unattached)
db = SQLAlchemy()
socketio = SocketIO(message_queue="redis://redis:6379", cors_allowed_origins='*')
#socketio = SocketIO(cors_allowed_origins='*')
login_manager = LoginManager()

def create_app():
    # 2. Create the Flask app
    app = Flask(__name__)
    app.config.from_object(Config)

    # 3. Bind extensions to the app
    db.init_app(app)
    socketio.init_app(app)
    login_manager.init_app(app)
    
    # Tells Flask-Login where to redirect if someone isn't logged in
    login_manager.login_view = 'auth.login'

    # 4. Set up the User Loader
    from app.models import Customer
    @login_manager.user_loader
    def load_user(user_id):
        return Customer.query.get(user_id)

    # 5. Create database tables
    with app.app_context():
        db.create_all()

    # 6. Register Blueprints (Routes)
    from app.routes.auth import auth_bp
    from app.routes.main import main_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)

    # 7. Import socket events so the app knows they exist
    from app import socket_events

    return app