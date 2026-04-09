from . import db

#FIGYELEM!!! EZ MÉG NINCS KÉSZ!!

class Address(db.Model):
    __tablename__ = 'addresses'
    id = db.Column(db.Integer, primary_key=True) #
    country = db.Column(db.String(100)) #
    city = db.Column(db.String(100)) #
    street = db.Column(db.String(255)) #

    #FIGYELEM!! EZ LEHET NEM KELL!!

    # Google Maps koordináták [cite: 54, 77]
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)