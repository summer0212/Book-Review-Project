from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config
from .models import db
import redis

# db = SQLAlchemy()
migrate = Migrate()

def create_app(config_class = Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app,db)
    # books_namespace.init_app(app)

    try:
        # Create the Redis client instance 
        app.redis_client = redis.from_url(app.config['REDIS_URL'], decode_responses=True)
        # Test the connection by sending a PING command
        app.redis_client.ping()
        print("Successfully connected to Redis!")
    except redis.exceptions.ConnectionError as e:
        print(f"FATAL: Could not connect to Redis. Please check your REDIS_URL and network.")
        print(f"Error details: {e}")
        
        raise e
   

    from .routes import api_bp
    app.register_blueprint(api_bp)

    return app
