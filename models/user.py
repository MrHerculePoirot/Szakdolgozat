from . import db
#Ez adja meg a felhasználónak azokat a képességeket, amik a bejelentkezéshez kellenek.
from flask_login import UserMixin #MI - Import pontos meghatározásához AI asszisztenciát vettem igénybe.


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    #User alapadatai
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))   
    phone = db.Column(db.String(20), nullable=True) 
    social_link = db.Column(db.String(200), nullable=True) # Nem kötelező, opcionális mező.
    is_active = db.Column(db.Boolean, default=False)
    
    # Aggregáció/asszociáció
    contact_id = db.Column(db.Integer, db.ForeignKey('phone_numbers.id'))
    address_id = db.Column(db.Integer, db.ForeignKey('addresses.id'))
    
    animals = db.relationship('Animal', backref='owner', lazy=True)#Ez a sor teszi lehetővé, hogy ha van egy felhasználóm listázhassam az összes állatát.