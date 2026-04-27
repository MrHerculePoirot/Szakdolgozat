from flask_sqlalchemy import SQLAlchemy #MI - Import pontos meghatározásához AI asszisztenciát vettem igénybe.
from flask_login import LoginManager #MI - Import pontos meghatározásához AI asszisztenciát vettem igénybe.

db = SQLAlchemy() #Itt jön létre maga az adatbázis-kezelő objektum.
login_manager = LoginManager() #Ez felel azért, hogy a rendszer megjegyezze, ki van bejelentkezve.

def init_app(app): #Applikáció
    db.init_app(app)
    login_manager.init_app(app)
    # Beállítjuk, hová irányítson a rendszer, ha bejelentkezés nélkül akarnak elérni valamit
    login_manager.login_view = 'login' 

@login_manager.user_loader
def load_user(user_id): #Itt a böngésző küld egy azonosítót és a függvény keresi meg a felhasználót az adatbázisban.
    from .user import User
    return User.query.get(int(user_id))