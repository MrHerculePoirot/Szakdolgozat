from . import db

#FIGYELEM!! EZ MÉG NINCS KÉSZ!!!

class Animal(db.Model):
    __tablename__ = 'animals'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    age = db.Column(db.Integer)
    status = db.Column(db.String(20)) # LOST/FOUND
    colour = db.Column(db.String(50))
    chip_id = db.Column(db.String(50))

    # Ezt ide tesszük, hogy minden alosztály használhassa anélkül, hogy ütközne
    breed = db.Column(db.String(100)) 
    

    type = db.Column(db.String(50))


    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    photo_path = db.Column(db.String(255), nullable=True)

    
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    

    home_address_id = db.Column(db.Integer, db.ForeignKey('addresses.id'))
    last_seen_address_id = db.Column(db.Integer, db.ForeignKey('addresses.id'))

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