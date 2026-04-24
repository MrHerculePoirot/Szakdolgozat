@echo off
:: UTF-8 kódolás beállítása az ékezetek miatt
chcp 65001 > nul

echo [1/4] Virtuális környezet aktiválása...
if not exist venv (
    echo Hiba: A 'venv' mappa nem található! Kérlek hozd létre: python -m venv venv
    pause
    exit /b
)
call venv\Scripts\activate

echo [2/4] Szükséges csomagok telepítése a requirements.txt alapján...
:: Ez a legfontosabb sor, ez telepíti a TensorFlow-t és az összes többi függőséget
pip install -r requirements.txt

echo [3/4] AI környezet és TensorFlow ellenőrzése...
python -c "import tensorflow as tf; print('TensorFlow verzió:', tf.__version__)"

echo [4/4] Flask szerver indítása...
python app.py
pause