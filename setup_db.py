import os
from flask_migrate import init, migrate, upgrade
from app import create_app, db

app = create_app()

with app.app_context():
    #MI - A migrációs környezet létrehozásához - és megértéséhez - AI asszisztenciát vettem igénybe.
    #Migrációs mappa létrehozása, ha még nincs
    if not os.path.exists('migrations'):
        print("Migrációs környezet inicializálása...")
        init()
    
    #Változások keresése
    print("Változások keresése...")
    migrate(message="Auto migration")
    
    #Adatbázis tényleges frissítése
    print("Adatbázis frissítése...")
    upgrade() #Adatvesztés nélkül
    print("Kész! Az adataid megmaradtak, a tábla bővült.")