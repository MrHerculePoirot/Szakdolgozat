import os
from flask_migrate import init, migrate, upgrade
from app import create_app, db

app = create_app()

with app.app_context():
    # 1. Migrációs mappa létrehozása, ha még nincs
    if not os.path.exists('migrations'):
        print("Migrációs környezet inicializálása...")
        init()
    
    # 2. Változások keresése (pl. az új last_seen_date mező)
    print("Változások keresése...")
    migrate(message="Auto migration")
    
    # 3. Adatbázis tényleges frissítése (ADATVESZTÉS NÉLKÜL)
    print("Adatbázis frissítése...")
    upgrade()
    print("Kész! Az adataid megmaradtak, a tábla bővült.")