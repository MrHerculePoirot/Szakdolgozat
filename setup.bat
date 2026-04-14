@echo off
echo [1/4] Virtualis kornyezet aktivalasa...
call venv\Scripts\activate


echo [2/4] Szukseges csomagok frissitese...
pip install flask flask-sqlalchemy flask-login python-dotenv

echo [3/4] Adatbazis es kornyezet ellenorzese...
python -c "import flask; print('Flask verzio:', flask.__version__)"

echo [4/4] Szerver inditasa...
python app.py
pause