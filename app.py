import os
import random
from flask import Flask, request, jsonify, render_template, redirect, url_for, flash
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

    # Konfiguráció
    basedir = os.path.abspath(os.path.dirname(__file__))
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'pet_finder.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'SECRETKEY'

    # Fájlfeltöltés beállításai
    UPLOAD_FOLDER = os.path.join('static', 'uploads')
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

    # Adatbázis inicializálása
    init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    with app.app_context():
        db.create_all()
        print("Adatbázis táblák sikeresen létrehozva!")

    # --- ÚTVONALAK ---

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
                is_active=True
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
                    flash("A fiókod még nincs hitelesítve!")
                    return redirect(url_for('login'))
                login_user(user)
                return redirect(url_for('index'))
            flash("Hibás adatok!")
            return redirect(url_for('login'))
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
            # 1. Helyszín adatok kinyerése
            country = request.form.get('country')
            city = request.form.get('city')
            postcode = request.form.get('postcode')
            street = request.form.get('street')

            # 2. Új helyszín (Address) létrehozása
            new_location = Address(
                country=country,
                city=city,
                postcode=postcode,
                street=street
            )
            db.session.add(new_location)
            db.session.flush()

            # 3. Chipszám validáció (15 jegyű szám)
            chip_id = request.form.get('chip_id')
            if chip_id and (not chip_id.isdigit() or len(chip_id) != 15):
                return "Hiba: A chipszámnak pontosan 15 számjegyből kell állnia!", 400

            # 4. Állat példányosítása típus alapján
            pet_type = request.form.get('type')
            if pet_type == 'dog':
                new_pet = Dog(breed=request.form.get('breed'))
            elif pet_type == 'cat':
                new_pet = Cat(breed=request.form.get('breed'))
            else:
                new_pet = Other(breed=request.form.get('breed'))

            # 5. Adatok feltöltése az új mezőkkel
            new_pet.name = request.form.get('name')
            new_pet.status = request.form.get('status')
            new_pet.colour = request.form.get('colour')
            new_pet.chip_id = chip_id
            new_pet.age = request.form.get('age')
            new_pet.age_unit = request.form.get('age_unit')
            new_pet.is_neutered = request.form.get('is_neutered') == 'true'
            new_pet.description = request.form.get('description')
            new_pet.user_id = current_user.id
            new_pet.location_id = new_location.id # Kapcsolat az új néven

            # 6. Fotó kezelése
            file = request.files.get('photo')
            if file and file.filename != '':
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                new_pet.photo_path = filename

            db.session.add(new_pet)
            db.session.commit()
            return redirect(url_for('my_pets'))
        return render_template('add_pet.html')

    @app.route('/my_pets')
    @login_required
    def my_pets():
        user_pets = Animal.query.filter_by(user_id=current_user.id).all()
        return render_template('my_pets.html', pets=user_pets)

    @app.route('/edit_pet/<int:pet_id>', methods=['GET', 'POST'])
    @login_required
    def edit_pet(pet_id):
        pet = Animal.query.get_or_404(pet_id)
        if pet.user_id != current_user.id:
            return "Nincs jogosultságod!", 403

        if request.method == 'POST':
            # Alapadatok frissítése
            pet.name = request.form.get('name')
            pet.status = request.form.get('status')
            pet.breed = request.form.get('breed')
            pet.colour = request.form.get('colour')
            pet.chip_id = request.form.get('chip_id')
            pet.age = request.form.get('age')
            pet.age_unit = request.form.get('age_unit')
            pet.is_neutered = request.form.get('is_neutered') == 'true'
            pet.description = request.form.get('description')

            # Helyszín frissítése (ha létezik a kapcsolat)
            if pet.location:
                pet.location.country = request.form.get('country')
                pet.location.city = request.form.get('city')
                pet.location.postcode = request.form.get('postcode')
                pet.location.street = request.form.get('street')
            
            db.session.commit()
            return redirect(url_for('my_pets'))
        return render_template('edit_pet.html', pet=pet)
    
    ######################xxxx
    @app.route('/pet/<int:pet_id>')
    def pet_detail(pet_id):
        # Lekérjük az állatot az ID alapján
        pet = Animal.query.get_or_404(pet_id)
        return render_template('pet_detail.html', pet=pet)
    #######################

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
    
    @app.route('/all_pets')
    def all_pets():
        all_animals = Animal.query.all()
        if len(all_animals) > 50:
            display_pets = random.sample(all_animals, 50)
        else:
            display_pets = all_animals
        return render_template('all_pets.html', pets=display_pets)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)