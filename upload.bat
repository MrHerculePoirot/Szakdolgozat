@echo off

git config --global user.email "balint.endrodi@gmail.com" 
git config --global user.name "Endrődi Bálint"

set /p comment="Legfrissebb állomány feltöltése"

echo [1/3] Fajlok hozzaadasa...
git add .

echo [2/3] Valtozasok rogzitese...
git commit -m "%comment%"

echo [3/3] Feltoltes a GitHubra...
git push origin main

echo.
echo Kesz!
pause