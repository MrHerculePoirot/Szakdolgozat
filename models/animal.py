from . import db

class Animal(db.Model):
    __tablename__ = 'animals'
    #Lentebb az állatok összes lehetséges adata.
    #Nem kötelező, hogy mindegyiknek legyen értéke
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    age = db.Column(db.Integer)
    age_unit = db.Column(db.String(20))
    gender = db.Column(db.String(20)) 
    status = db.Column(db.String(20))
    colour = db.Column(db.String(50))
    chip_id = db.Column(db.String(50))
    #Ezt azért így írjuk, hogy minden alosztály használhassa anélkül, hogy ütközne.
    breed = db.Column(db.String(100))
    last_seen_date = db.Column(db.Date, nullable=True)
    is_neutered = db.Column(db.Boolean, default=False)
    type = db.Column(db.String(50))
    description = db.Column(db.Text, nullable=True)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    photo_path = db.Column(db.String(255), nullable=True)    
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    #Lentebb lévő két változó köti össze az állatot egy konkrét címmel az addresses segítségével.
    location_id = db.Column(db.Integer, db.ForeignKey('addresses.id'))
    location = db.relationship('Address', foreign_keys=[location_id])
    chip_id = db.Column(db.String(15), nullable=True) #A valid chipszám formátuma 15 számjegyből áll.

    __mapper_args__ = {
        'polymorphic_identity': 'animal',
        'polymorphic_on': type #Az adatbázisban egyetlen tábla van, de a type oszlop alapján a Flask tudja, hogy az adott sor faját.
    }

class Dog(Animal):
    __mapper_args__ = {'polymorphic_identity': 'dog'}

class Cat(Animal):
    __mapper_args__ = {'polymorphic_identity': 'cat'}

class Other(Animal):
    __mapper_args__ = {'polymorphic_identity': 'other'}