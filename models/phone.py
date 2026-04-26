from . import db

class PhoneNumber(db.Model):
    __tablename__ = 'phone_numbers'
    id = db.Column(db.Integer, primary_key=True)
    country_id = db.Column(db.Integer)
    # Figyelj a névre: phone_number
    phone_number = db.Column(db.String(20))