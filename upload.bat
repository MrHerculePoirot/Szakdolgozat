@echo off
:: UTF-8 kódolás az ékezetek miatt
chcp 65001 > nul

:: Itt a kettőspont után kell várnia a szöveget
set /p comment="Add meg a módosítás leírását: "

:: Ha üresen hagyod, kap egy dátumos alapértelmezettet
if "%comment%"=="" set comment="Automatikus frissites - %date% %time%"

echo [1/3] Fajlok hozzaadasa...
git add .

echo [2/3] Valtozasok rogzitese...
:: Az idézőjelek a %comment% körül kritikusak!
git commit -m "%comment%"

echo [3/3] Feltoltes a GitHubra...
git push origin main

echo.
echo KESZ! Minden fajl fent van a GitHubon.
pause