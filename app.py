import os
import random
from flask_migrate import Migrate, upgrade
from flask import Flask, request, jsonify, render_template, redirect, url_for, flash
from dotenv import load_dotenv
from datetime import datetime
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

def load_list(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        # Csak azokat a sorokat tartjuk meg, amik nem üresek és nem [source...]-szal kezdődnek
        return [line.strip() for line in f if line.strip() and not line.startswith('[')]

# Listák betöltése a fájlokból
COLORS = load_list('colors.txt')
DOG_BREEDS = load_list('dog_breeds.txt')
CAT_BREEDS = load_list('cat_breeds.txt')
OTHER_BREEDS = load_list('other_breeds.txt')
# Ez az összesített lista a szűréshez kell majd
ALL_BREEDS = sorted(list(set(DOG_BREEDS + CAT_BREEDS + OTHER_BREEDS)))

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
    migrate = Migrate(app, db)


    with app.app_context():
        # Ez a sor automatikusan frissíti az adatbázist indításkor
        if os.path.exists('migrations'):
            upgrade()
        print("Adatbázis sémák ellenőrizve és frissítve!")

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
        all_pets = Animal.query.all()
        pets_metadata = []
        
        for pet in all_pets:
            if pet.location:
                loc = pet.location
                full_addr = f"{loc.postcode} {loc.city}, {loc.street}, {loc.country}"
                owner_phone = "Nincs megadva"
                if pet.owner and pet.owner.phone:
                    owner_phone = pet.owner.phone
                
                pets_metadata.append({
                    'id': pet.id,
                    'name': pet.name or "Névtelen állat",
                    'status': pet.status,
                    'full_address': f"{pet.location.city}, {pet.location.street}",
                    'type': pet.type,
                    'photo_path': pet.photo_path, # ÚJ: Kell a kártyához
                    'owner_phone': owner_phone    # ÚJ: Kell a kártyához
                 })
        
        # Itt a pets_metadata-t KELL átadni, amit az imént töltöttél fel adatokkal!
        return render_template('map.html', api_key=api_key, pets_metadata=pets_metadata)
    
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
            ##############xx
            last_seen_str = request.form.get('last_seen_date')
            last_seen_dt = None
            if request.form.get('status') == 'LOST' and last_seen_str:
                try:
                    last_seen_dt = datetime.strptime(last_seen_str, '%Y-%m-%d').date()
                except ValueError:
                    last_seen_dt = None
            ###########xxx
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
            new_pet.gender = request.form.get('gender')
            new_pet.is_neutered = request.form.get('is_neutered') == 'true'
            new_pet.description = request.form.get('description')
            new_pet.user_id = current_user.id
            new_pet.location_id = new_location.id # Kapcsolat az új néven
            new_pet.last_seen_date = last_seen_dt  # Adatbázisba írjuk

            # 6. Több fotó kezelése és egyedi mappába rendezése
            files = request.files.getlist('photo')[:4]
            filenames = []
            
            if files and files[0].filename != '':
                # Először elmentjük az állatot, hogy legyen ID-ja
                db.session.add(new_pet)
                db.session.flush() # Ez generálja le az ID-t az adatbázisban mentés előtt

                # Létrehozzuk a mappát: static/uploads/pet_ID
                pet_folder_name = f'pet_{new_pet.id}'
                pet_dir = os.path.join(app.config['UPLOAD_FOLDER'], pet_folder_name)
                
                if not os.path.exists(pet_dir):
                    os.makedirs(pet_dir)

                for file in files:
                    if file.filename != '':
                        filename = secure_filename(file.filename)
                        # A képet az új, saját mappájába mentjük
                        file.save(os.path.join(pet_dir, filename))
                        filenames.append(filename)
                
                # A fájlneveket vesszővel elválasztva mentjük az adatbázisba
                new_pet.photo_path = ",".join(filenames)
            
            db.session.commit()
            return redirect(url_for('my_pets'))
        # app.py - Keresd meg a függvény végét:
        return render_template('add_pet.html', 
                               colors=COLORS, 
                               dog_breeds=DOG_BREEDS, 
                               cat_breeds=CAT_BREEDS, 
                               other_breeds=OTHER_BREEDS)
        ##return render_template('add_pet.html')

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
            pet.gender = request.form.get('gender')

            # Helyszín frissítése (ha létezik a kapcsolat)
            if pet.location:
                pet.location.country = request.form.get('country')
                pet.location.city = request.form.get('city')
                pet.location.postcode = request.form.get('postcode')
                pet.location.street = request.form.get('street')
            
            db.session.commit()
            return redirect(url_for('my_pets'))
        # app.py - Itt is minden lista kell a módosításhoz:
        return render_template('edit_pet.html', 
                            pet=pet, 
                            colors=COLORS, 
                            dog_breeds=DOG_BREEDS, 
                            cat_breeds=CAT_BREEDS, 
                            other_breeds=OTHER_BREEDS)
        ##return render_template('edit_pet.html', pet=pet)
    
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
        query = Animal.query

        # 1. Típus szűrés (ez már megvan)
        pet_type = request.args.get('type')
        if pet_type and pet_type != 'all':
            query = query.filter(Animal.type == pet_type)

        # --- EZ HIÁNYZOTT: Fajta szűrés ---
        breed_search = request.args.get('breed')
        if breed_search and breed_search != 'all' and breed_search != '':
            query = query.filter(Animal.breed == breed_search)


        # ÚJ: Státusz szűrés (LOST/FOUND/ADOPTION)
        status_search = request.args.get('status')
        if status_search and status_search != 'all':
            query = query.filter(Animal.status == status_search)

        # 2. NÉV szűrés (külön mező a HTML-ben)
        name_search = request.args.get('name', '').strip()
        if name_search:
            query = query.filter(Animal.name.ilike(f'%{name_search}%'))

        #######
        gender_search = request.args.get('gender')
        if gender_search and gender_search != 'all':
            query = query.filter(Animal.gender == gender_search)

        # 3. CHIPSZÁM szűrés (külön mező a HTML-ben)
        chip_search = request.args.get('chip_id', '').strip()
        if chip_search:
            query = query.filter(Animal.chip_id == chip_search)

        # 4. Helyszín szűrés
        loc_search = request.args.get('location', '').strip()
        if loc_search:
            query = query.join(Address).filter(
                (Address.city.ilike(f'%{loc_search}%')) | 
                (Address.country.ilike(f'%{loc_search}%'))
            )

        # 5. Kor és MÉRTÉKEGYSÉG szűrés
            # Kor szűrése az app.py-ban
        age_min = request.args.get('age_min')
        age_max = request.args.get('age_max')
        age_unit = request.args.get('age_unit')

        # Csak akkor szűrünk az egységre, ha van megadva számérték (min vagy max)
        if (age_min and age_min.strip()) or (age_max and age_max.strip()):
            if age_min and age_min.strip():
                query = query.filter(Animal.age >= int(age_min))
            if age_max and age_max.strip():
                query = query.filter(Animal.age <= int(age_max))
            # Mivel van számérték, ekkor már kötelezően szűrünk a kiválasztott egységre is
            if age_unit:
                query = query.filter(Animal.age_unit == age_unit)

        display_pets = query.all()
        
        # Limit csak ha nincs szűrés
        if not any([pet_type != 'all' and pet_type, name_search, chip_search, loc_search, age_min, age_max]) and len(display_pets) > 50:
            display_pets = random.sample(display_pets, 50)


        # app.py javítás
        return render_template('all_pets.html', 
                            pets=display_pets, 
                            colors=COLORS, 
                            all_breeds=ALL_BREEDS,
                            dog_breeds=DOG_BREEDS,  # EZ HIÁNYZOTT
                            cat_breeds=CAT_BREEDS,  # EZ HIÁNYZOTT
                            other_breeds=OTHER_BREEDS) # EZ HIÁNYZOTT
            ##return render_template('all_pets.html', pets=display_pets)
    """
        return render_template('all_pets.html', 
                               pets=display_pets, 
                               colors=COLORS, 
                               all_breeds=ALL_BREEDS) #other_breeds=OTHER_BREEDS
        """
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)