from . import db

#FIGYELEM!! EZ MÉG NINCS KÉSZ!!!

class Animal(db.Model):
    __tablename__ = 'animals'
    id = db.Column(db.Integer, primary_key=True) #
    type = db.Column(db.String(50)) # Az öröklődéshez szükséges (discriminator)
    
    name = db.Column(db.String(100)) #
    age = db.Column(db.Integer) #
    status = db.Column(db.String(20)) # LOST/FOUND
    colour = db.Column(db.String(50)) #
    chip_id = db.Column(db.String(50)) #
    
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False) #
    
    # Helyszínek
    home_address_id = db.Column(db.Integer, db.ForeignKey('addresses.id'))
    last_seen_address_id = db.Column(db.Integer, db.ForeignKey('addresses.id'))

    __mapper_args__ = {
        'polymorphic_identity': 'animal',
        'polymorphic_on': type
    }

class Dog(Animal):
    breed = db.Column(db.String(100)) #
    __mapper_args__ = {'polymorphic_identity': 'dog'}

class Cat(Animal):
    breed = db.Column(db.String(100)) #
    __mapper_args__ = {'polymorphic_identity': 'cat'}

class Other(Animal):
    breed = db.Column(db.String(100)) # Itt a faj megnevezése
    __mapper_args__ = {'polymorphic_identity': 'other'}