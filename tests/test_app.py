import pytest
from unittest.mock import patch
from app import create_app, db
from models.user import User
from models.animal import Animal, Dog, Cat
from werkzeug.security import generate_password_hash


# Ez a fixture minden egyes teszt előtt lefut: létrehoz egy tiszta,
# memóriában élő tesztadatbázist, így a tesztek nem piszkítják össze az éles pet_finder.db fájlt.
@pytest.fixture
def client():
    """Tesztkörnyezet inicializálása memóriában futó adatbázissal."""
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:' # Csak a RAM-ban létezik a teszt idejére
    app.config['WTF_CSRF_ENABLED'] = False
    app.config['MAIL_SUPPRESS_SEND'] = True # Tesztelés közben ne küldjön valódi e-maileket

    with app.test_client() as client:
        with app.app_context():
            db.create_all() # Táblák létrehozása a memóriában
            yield client # Itt fut le az aktuális tesztfüggvény
            db.session.remove()
            db.drop_all() # Teszt után mindent törlünk, hogy a következő tiszta lappal induljon


def test_polymorphic_animal_models(client):
    """1. Egységteszt: OOP öröklődés és diszkriminátor ellenőrzése."""
    # Létrehozunk egy teszt felhasználót, akihez az állatokat kötjük
    user = User(username="tesztuser", email="teszt@pelda.hu", password_hash="hash", is_active=True)
    db.session.add(user)
    db.session.commit()

    # Két különböző leszármazott osztályt (Dog, Cat) mentünk le
    dog = Dog(name="Bodri", breed="Vizsla", status="LOST", user_id=user.id)
    cat = Cat(name="Cirmi", breed="Maine Coon", status="FOUND", user_id=user.id)
    db.session.add_all([dog, cat])
    db.session.commit()

    # A közös Animal ősosztályon keresztül kérdezzük le őket, és ellenőrizzük,
    # hogy az SQLAlchemy helyesen állította-e be a típusukat (polimorfizmus)
    animals = Animal.query.all()
    assert len(animals) == 2
    assert isinstance(animals[0], Dog)
    assert animals[0].type == 'dog'
    assert isinstance(animals[1], Cat)
    assert animals[1].type == 'cat'

#MI - A függvény megírásához AI asszisztenciát vettem igénybe
def test_unauthorized_access_redirect(client):
    """2. Egységteszt: Jogosultságkezelés (@login_required ellenőrzése)."""
    # Bejelentkezés nélkül próbáljuk megnyitni a védett /add_pet oldalt
    response = client.get('/add_pet')
    # Elvárjuk, hogy átirányítson (302) a bejelentkező felületre
    assert response.status_code == 302
    assert '/login' in response.headers['Location']


def test_chip_id_validation(client):
    """3. Egységteszt: 15 jegyű chipszám validáció negatív tesztesete."""
    # Létrehozunk és beléptetünk egy felhasználót, mert a bejelentéshez be kell jelentkezni
    user = User(
        username="gazdi",
        email="gazdi@pelda.hu",
        password_hash=generate_password_hash("titok123"),
        is_active=True
    )
    db.session.add(user)
    db.session.commit()

    client.post('/login', data={'email': 'gazdi@pelda.hu', 'password': 'titok123'})

    # Szándékosan hibás (nem 15 számjegyű) chipszámmal küldjük el az űrlapot
    response = client.post('/add_pet', data={
        'status': 'LOST',
        'type': 'dog',
        'breed': 'Beagle',
        'country': 'Magyarország',
        'city': 'Budapest',
        'chip_id': '12345'  # Hibás formátum!
    })
    # Elvárjuk, hogy a szerver 400-as (Bad Request) hibával utasítsa el
    assert response.status_code == 400


# A @patch lecseréli a valódi MobileNetV2 képelemző függvényt egy előre beállított válaszra,
# így a teszt másodpercek alatt lefut valódi képfájl és neurális háló futtatása nélkül.
@patch('app.analyze_pet_image')
def test_ai_endpoint_with_mock(mock_analyze, client):
    """4. Egységteszt: AI végpont tesztelése a nehéz ML modell mockolásával."""
    # Megadjuk, mit adjon vissza az ál-AI függvény, ha meghívják
    mock_analyze.return_value = {'breed': 'Maine Coon', 'confidence': 89.5}

    # Felhasználó és egy fotóval rendelkező állat rögzítése az adatbázisban
    user = User(
        username="ai_teszt",
        email="ai@pelda.hu",
        password_hash=generate_password_hash("titok123"),
        is_active=True
    )
    db.session.add(user)
    db.session.commit()

    pet = Cat(name="Lajos", breed="Maine Coon", status="LOST", user_id=user.id, photo_path="lajos.jpg")
    db.session.add(pet)
    db.session.commit()

    # Bejelentkezés után meghívjuk az AI elemző API végpontot
    client.post('/login', data={'email': 'ai@pelda.hu', 'password': 'titok123'})
    response = client.get(f'/api/analyze/{pet.id}')
    
    # Ellenőrizzük a sikeres (200) választ és a visszakapott JSON adatokat
    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data['breed'] == 'Maine Coon'
    assert json_data['confidence'] == 89.5