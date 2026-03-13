@echo off
REM Do'kon Omborini Boshqarish Tizimi - Startup Script
REM Loyiha serverini ishga tushish uchun

echo.
echo ======================================
echo Do'kon Omborini Boshqarish Tizimi v1.0
echo ======================================
echo.

REM Virtual Environment ni faollashtirish
call .venv\Scripts\activate.bat

if errorlevel 1 (
    echo ERROR: Virtual environment ni faollashtirish xato!
    pause
    exit /b 1
)

echo [OK] Virtual environment faollashtirildi
echo.

REM Fayllar mavjudligini tekshirish
if not exist "db.sqlite3" (
    echo [INFO] Database topilmadi. Migratsiyalar bajarilmoqda...
    python manage.py migrate
)

echo.
echo [OK] Xamdamlik tekshiruvi o'tdi
echo.

echo ======================================
echo Server ishga tushurilmoqda...
echo ======================================
echo.
echo Web sahifasi: http://localhost:8000/
echo Admin paneli: http://localhost:8000/admin/
echo.
echo Serverni tugatish uchun: CTRL + C
echo.

python manage.py runserver
