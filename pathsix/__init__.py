from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from config import Config

db = SQLAlchemy()
mail = Mail()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    mail.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    from pathsix.main.routes import main
    from pathsix.errors.handlers import errors
    from pathsix.pathsix_crm.crm_main.routes import crm_main
    from pathsix.pathsix_crm.customer.routes import customer
    from pathsix.pathsix_crm.users.routes import users
    
    app.register_blueprint(main)
    app.register_blueprint(crm_main)
    app.register_blueprint(customer)
    app.register_blueprint(users)
    app.register_blueprint(errors)

    return app