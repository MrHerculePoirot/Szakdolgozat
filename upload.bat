@echo off
:: Ha nem UTF-8 a kódolás az ékezeteket nem tudja nromálisan kezelniss
chcp 65001 > nul

set /p comment="Add meg a módosítás leírását: "

:: Ha nem írok semmit akk dátum szerint frissíti/nevezi el
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