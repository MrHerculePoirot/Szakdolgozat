from . import db
from flask_login import UserMixin

class User(db.Model):
    __tablename__ = 'users'
    
    #FIGYELEM EZ MÉG NINCS KÉSZ


    id = db.Column(db.Integer, primary_key=True) #
    email = db.Column(db.String(120), unique=True, nullable=False) #
    google_id = db.Column(db.String(128), unique=True, nullable=False) #
    social_link = db.Column(db.Text) #
    
    # Kapcsolatok (Aggregation/Association)
    contact_id = db.Column(db.Integer, db.ForeignKey('phone_numbers.id')) #
    address_id = db.Column(db.Integer, db.ForeignKey('addresses.id')) #
    
    animals = db.relationship('Animal', backref='owner', lazy=True) #