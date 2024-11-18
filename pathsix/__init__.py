from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from config import Config

# Initialize the Flask app and load config
app = Flask(__name__)
app.config.from_object(Config)

# Initialize extensions
db = SQLAlchemy(app)
mail = Mail(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'

# Import routes at the end to avoid circular imports
from pathsix.main.routes import main
from pathsix.pathsix_crm.crm_main.routes import crm_main
from pathsix.pathsix_crm.customer.routes import customer
from pathsix.pathsix_crm.users.routes import users

# Register blueprints
app.register_blueprint(main)
app.register_blueprint(crm_main) 
app.register_blueprint(customer)
app.register_blueprint(users)