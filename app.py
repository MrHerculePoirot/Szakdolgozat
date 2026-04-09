import os
from flask import Flask, request, jsonify
from flask_login import login_required, current_user
from models import db, init_app
from models.animal import Dog, Cat, Other
from models.user import User

def create_app():
    app = Flask(__name__)

    # Konfiguráció - SQLite adatbázis fájl létrehozása helyben [cite: 61]
    basedir = os.path.abspath(os.path.dirname(__file__))
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'pet_finder.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'titkos-kulcs-a-szakdolgozathoz'

    # Adatbázis inicializálása [cite: 38]
    init_app(app)

    with app.app_context():
        # Ez hozza létre a .db fájlt és a táblákat a modellek alapján
        db.create_all()
        print("Adatbázis táblák sikeresen létrehozva!")

    @app.route('/add_animal', methods=['POST'])
    @login_required # Csak hitelesített felhasználó érheti el 
    def add_animal():
        data = request.json
        pet_type = data.get('type')
        
        # A diagram alapján példányosítjuk a megfelelő alosztályt
        if pet_type == 'dog':
            new_pet = Dog(breed=data.get('breed'))
        elif pet_type == 'cat':
            new_pet = Cat(breed=data.get('breed'))
        else:
            new_pet = Other(breed=data.get('breed'))
            
        # Közös attribútumok beállítása
        new_pet.name = data.get('name')
        new_pet.status = data.get('status', 'LOST')
        new_pet.colour = data.get('colour')
        new_pet.chip_id = data.get('chip_id')
        
        # A kapcsolat rögzítése a bejelentkezett felhasználóval
        new_pet.owner = current_user 
        
        db.session.add(new_pet)
        db.session.commit()
    
    return jsonify({"message": "Sikeres rögzítés!"}), 201

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)