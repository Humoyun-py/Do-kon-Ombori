#!/bin/bash
# Do'kon Omborini Boshqarish Tizimi - Startup Script
# Loyiha serverini ishga tushish uchun (Linux/Mac)

echo ""
echo "======================================"
echo "Do'kon Omborini Boshqarish Tizimi v1.0"
echo "======================================"
echo ""

# Virtual Environment ni faollashtirish
source .venv/bin/activate

if [ $? -ne 0 ]; then
    echo "ERROR: Virtual environment ni faollashtirish xato!"
    exit 1
fi

echo "[OK] Virtual environment faollashtirildi"
echo ""

# Fayllar mavjudligini tekshirish
if [ ! -f "db.sqlite3" ]; then
    echo "[INFO] Database topilmadi. Migratsiyalar bajarilmoqda..."
    python manage.py migrate
fi

echo ""
echo "[OK] Xamdamlik tekshiruvi o'tdi"
echo ""

echo "======================================"
echo "Server ishga tushurilmoqda..."
echo "======================================"
echo ""
echo "Web sahifasi: http://localhost:8000/"
echo "Admin paneli: http://localhost:8000/admin/"
echo ""
echo "Serverni tugatish uchun: CTRL + C"
echo ""

python manage.py runserver
