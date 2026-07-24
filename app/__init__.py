from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_migrate import Migrate
from config import Config

# Initialize extensions globally
db = SQLAlchemy()
jwt = JWTManager()
cors = CORS()
migrate = Migrate()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Bind extensions to the app instance
    db.init_app(app)
    jwt.init_app(app)
    cors.init_app(app, resources={r"/api/*": {"origins": "*", "allow_headers": "*", "methods": ["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"]}}, supports_credentials=True)
    migrate.init_app(app, db)

    from app.routes import api_bp
    app.register_blueprint(api_bp, url_prefix='/api')

    return app