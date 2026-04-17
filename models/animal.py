from . import db

#FIGYELEM!! EZ MÉG NINCS KÉSZ!!!

class Animal(db.Model):
    __tablename__ = 'animals'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    age = db.Column(db.Integer)
    age_unit = db.Column(db.String(20))
    status = db.Column(db.String(20)) # LOST/FOUND
    colour = db.Column(db.String(50))
    chip_id = db.Column(db.String(50))

    # Ezt ide tesszük, hogy minden alosztály használhassa anélkül, hogy ütközne
    breed = db.Column(db.String(100)) 
    
    is_neutered = db.Column(db.Boolean, default=False)
    type = db.Column(db.String(50))
    description = db.Column(db.Text, nullable=True)


    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    photo_path = db.Column(db.String(255), nullable=True)

    
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    ##user = db.relationship('User', backref='animals')
    

    # A korábbi home_address_id és last_seen_address_id helyett:
    location_id = db.Column(db.Integer, db.ForeignKey('addresses.id'))

    # Adjunk hozzá egy kapcsolatot is a könnyebb eléréshez:
    location = db.relationship('Address', foreign_keys=[location_id])
    
    
    chip_id = db.Column(db.String(15), nullable=True)

    __mapper_args__ = {
        'polymorphic_identity': 'animal',
        'polymorphic_on': type
    }

class Dog(Animal):
    __mapper_args__ = {'polymorphic_identity': 'dog'}

class Cat(Animal):
    __mapper_args__ = {'polymorphic_identity': 'cat'}

class Other(Animal):
    __mapper_args__ = {'polymorphic_identity': 'other'}