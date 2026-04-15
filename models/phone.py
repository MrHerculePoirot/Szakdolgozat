from . import db

#FIGYELEM! MÉG EZ SINCS KÉSZ!!!!!!

class PhoneNumber(db.Model):
    __tablename__ = 'phone_numbers'
    id = db.Column(db.Integer, primary_key=True)
    country_id = db.Column(db.Integer)
    phone_number = db.Column(db.String(20))