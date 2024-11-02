from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from config import Config

# Initialize the Flask app and load config
app = Flask(__name__)
app.config.from_object(Config)

# Initialize extensions
db = SQLAlchemy(app)
mail = Mail(app)

# Import routes at the end to avoid circular imports
from pathsix import routes
