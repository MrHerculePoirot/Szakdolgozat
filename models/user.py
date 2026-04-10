from . import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    
    #FIGYELEM EZ MÉG NINCS KÉSZ


    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    ##google_id = db.Column(db.String(128), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    
    phone = db.Column(db.String(20), nullable=True) 
    social_link = db.Column(db.String(200), nullable=True) # Opcionális mező
    
    is_active = db.Column(db.Boolean, default=False)
    
    # Kapcsolatok (Aggregation/Association)
    contact_id = db.Column(db.Integer, db.ForeignKey('phone_numbers.id'))
    address_id = db.Column(db.Integer, db.ForeignKey('addresses.id'))
    
    animals = db.relationship('Animal', backref='owner', lazy=True)