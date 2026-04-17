import os
from flask import Flask, request, jsonify, render_template, redirect, url_for
from dotenv import load_dotenv
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from models import db, init_app
from models.address import Address
from models.phone import PhoneNumber
from models.user import User
from models.animal import Animal, Dog, Cat, Other

# Környezeti változók betöltése
load_dotenv()

def create_app():
    app = Flask(__name__)

    # Konfig -> SQLite adatbázis file létrehozása
    basedir = os.path.abspath(os.path.dirname(__file__))
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'pet_finder.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'SECRETKEY'

    # Fájlfeltöltés beállításai
    UPLOAD_FOLDER = os.path.join('static', 'uploads')
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

    # Adatbázis létrehozása
    init_app(app)

    # Login Manager beállítása
    login_manager = LoginManager()
    login_manager.login_view = 'login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    with app.app_context():
        # .db file és táblák létrehozása
        db.create_all()
        print("Adatbázis táblák sikeresen létrehozva!")

    # ---Útvonalak---

    @app.route('/')
    def index():
        api_key = os.getenv('GOOGLE_MAPS_API_KEY')
        animals = Animal.query.all()
        return render_template('map.html', api_key=api_key, animals=animals)
    
    @app.route('/register', methods=['GET', 'POST'])
    def register():
        if request.method == 'POST':
            hashed_pw = generate_password_hash(request.form.get('password'))
            new_user = User(
                username=request.form.get('username'),
                email=request.form.get('email'),
                password_hash=hashed_pw,
                phone=request.form.get('phone'),
                social_link=request.form.get('social_link'),
                is_active=True # IDEIGLENESEN: Aktív lesz a teszteléshez - nem megy a visszaigazolás
            )
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('login'))
        return render_template('register.html')

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            user = User.query.filter_by(email=request.form.get('email')).first()
            if user and check_password_hash(user.password_hash, request.form.get('password')):
                if not user.is_active:
                    return "A fiókod még nincs hitelesítve! Ellenőrizd az e-mailedet.", 403
            
                login_user(user)
                return redirect(url_for('index'))
            return "Hibás adatok!", 401
        return render_template('login.html')
    
    @app.route('/logout')
    @login_required
    def logout():
        logout_user()
        return redirect(url_for('index'))
    
    @app.route('/add_pet', methods=['GET', 'POST'])
    @login_required
    def add_pet():
        if request.method == 'POST':
            # 1. Minden adat kinyerése az űrlapról (Cím + Állat infók)
            country = request.form.get('country')
            city = request.form.get('city')
            postcode = request.form.get('postcode')
            street = request.form.get('street')
            
            # Chipszám lekérése a validációhoz
            chip_id = request.form.get('chip_id')
            if chip_id and (not chip_id.isdigit() or len(chip_id) != 15):
                return "Hiba: A chipszámnak pontosan 15 számjegyből kell állnia!", 400

            # 2. Új cím objektum létrehozása
            new_address = Address(
                country=country,
                city=city,
                postcode=postcode,
                street=street
            )
            db.session.add(new_address)
            db.session.flush() # Ez generálja le az ID-t a mentés előtt

            # 3. Állat példányosítása a típusa alapján
            pet_type = request.form.get('type')
            if pet_type == 'dog':
                new_pet = Dog(breed=request.form.get('breed'))
            elif pet_type == 'cat':
                new_pet = Cat(breed=request.form.get('breed'))
            else:
                new_pet = Other(breed=request.form.get('breed'))

            # 4. Az állat adatainak feltöltése és összekapcsolása
            new_pet.name = request.form.get('name')
            new_pet.status = request.form.get('status')
            new_pet.colour = request.form.get('colour')
            new_pet.chip_id = chip_id
            new_pet.age = request.form.get('age')
            new_pet.age_unit = request.form.get('age_unit')
            new_pet.is_neutered = request.form.get('is_neutered') == 'true'
            new_pet.description = request.form.get('description')
            new_pet.user_id = current_user.id
            new_pet.last_seen_address_id = new_address.id # Itt kapcsoljuk össze!

            # 5. Fotó kezelése
            file = request.files.get('photo')
            if file and file.filename != '':
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                new_pet.photo_path = filename

            # 6. Végső mentés az adatbázisba
            db.session.add(new_pet)
            db.session.commit()
            return redirect(url_for('my_pets'))
            
        return render_template('add_pet.html')

    @app.route('/add_animal', methods=['POST'])
    @login_required 
    def add_animal():
        data = request.json
        pet_type = data.get('type')
        
        if pet_type == 'dog':
            new_pet = Dog(breed=data.get('breed'))
        elif pet_type == 'cat':
            new_pet = Cat(breed=data.get('breed'))
        else:
            new_pet = Other(breed=data.get('breed'))
            
        new_pet.name = data.get('name')
        new_pet.status = data.get('status', 'LOST')
        new_pet.colour = data.get('colour')
        new_pet.chip_id = data.get('chip_id')
        new_pet.latitude = data.get('latitude')
        new_pet.longitude = data.get('longitude')
        new_pet.user_id = current_user.id
        
        db.session.add(new_pet)
        db.session.commit()
    
        return jsonify({"message": "Sikeres rögzítés!"}), 201
    
    @app.route('/my_pets')
    @login_required
    def my_pets():
        user_pets = Animal.query.filter_by(user_id=current_user.id).all()
        return render_template('my_pets.html', pets=user_pets)

    @app.route('/delete_pet/<int:pet_id>', methods=['POST'])
    @login_required
    def delete_pet(pet_id):
        pet = Animal.query.get_or_404(pet_id)
        if pet.user_id != current_user.id:
            return "Nincs jogosultságod!", 403
        
        if pet.photo_path:
            try:
                os.remove(os.path.join(app.config['UPLOAD_FOLDER'], pet.photo_path))
            except:
                pass 

        db.session.delete(pet)
        db.session.commit()
        return redirect(url_for('my_pets'))

    @app.route('/edit_pet/<int:pet_id>', methods=['GET', 'POST'])
    @login_required
    def edit_pet(pet_id):
        pet = Animal.query.get_or_404(pet_id)
        if pet.user_id != current_user.id:
            return "Nincs jogosultságod!", 403

        if request.method == 'POST':
            pet.name = request.form.get('name')
            pet.status = request.form.get('status')
            pet.colour = request.form.get('colour')
            pet.chip_id = request.form.get('chip_id')
            pet.breed = request.form.get('breed')
            
            db.session.commit()
            return redirect(url_for('my_pets'))
            
        return render_template('edit_pet.html', pet=pet)
    
    @app.route('/all_pets')

    def all_pets():
        # Az összes állat lekérése - egylőre mindegy, hogy LOST/FOUND
        all_animals = Animal.query.all()
        
        # Random max 50 db kiválasztása
        if len(all_animals) > 50:
            display_pets = random.sample(all_animals, 50)
        else:
            display_pets = all_animals
            
        return render_template('all_pets.html', pets=display_pets)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)