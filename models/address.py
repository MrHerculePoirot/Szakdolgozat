from . import db

class Address(db.Model): #Ez fogja tárolni a földrajzi adatokat. Ilyen objektumokat kap a térkép, ami stringgé alakul.
    __tablename__ = 'addresses'
    id = db.Column(db.Integer, primary_key=True)
    country = db.Column(db.String(100))
    city = db.Column(db.String(100))
    street = db.Column(db.String(255))
    postcode = db.Column(db.String(20))

    # Google Maps koordináták potenciális bővítéshez.
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)