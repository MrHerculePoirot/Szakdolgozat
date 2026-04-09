from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
login_manager = LoginManager()

#FIGYELEM! MÉG EZ SINCS KÉSZ!

def init_app(app):
    db.init_app(app)
    login_manager.init_app(app)
    # Beállítjuk, hová irányítson a rendszer, ha bejelentkezés nélkül akarnak elérni valamit
    login_manager.login_view = 'login' 

@login_manager.user_loader
def load_user(user_id):
    from .user import User
    return User.query.get(int(user_id))