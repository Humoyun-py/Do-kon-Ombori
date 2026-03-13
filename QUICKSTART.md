"""
Quick Start Guide - Do'kon Omborini Boshqarish Tizimi
"""

# LOYIHANI O'RNATISH VA ISHGA TUSHIRISH

## 1. LOYIHANING HOLATI
✅ Loyiha muvaffaqiyatli yaratildi!
✅ Database o'rnatildi
✅ Boshlang'ich ma'lumotlar yuklandi
✅ Django server ishga tayyor

## 2. ADMIN AKKAUNTINI YARATISH

Admin akkauntini yaratish uchun terminal oyna yoki PowerShell da quyidagi buyrug'ni bajaring:

```powershell
python manage.py createsuperuser
```

U'zingizni ma'lumotlarni kiriting:
- Username: (misol: admin)
- Email: (misol: admin@example.com)  
- Password: (xavfsiz parol tanlang)

## 3. SERVER ISHGA TUSHIRISH

```powershell
python manage.py runserver
```

Keyin brauzerda quyidagi manzilni oching:
- Web sahifa: http://localhost:8000/
- Admin paneli: http://localhost:8000/admin/

## 4. TELEGRAM BOTNI O'RNATISH (IXTIYORIY)

1. Telegram da @BotFather bilan suhbat oching
2. `/newbot` buyrug'ini yuboring
3. Bot uchun nomi va username kiriting
4. OAuth tokenni oching (misol: 1234567890:ABCDefGhIjKlmNopQrStUvWxYaZaBcDeFg)
5. `.env` faylida TELEGRAM_BOT_TOKEN qiymati o'zlashtiring:

```
TELEGRAM_BOT_TOKEN=1234567890:ABCDefGhIjKlmNopQrStUvWxYaZaBcDeFg
```

6. Botni ishga tushiring (yangi terminal oynasida):
```powershell
python bot/handlers.py
```

## 5. LOISH BOSHLANG'ICH MA'LUMOTLAR

Boshlang'ich kategorikalar, yetkazib beruvchilar va mahsulotlar allaqachon yuklangan:

### Kategoriyalar:
- Oziq-ovqat
- Ichimliklar
- Tozalash vositalari
- Elektronika
- Poyabzal

### Yetkazib beruvchilar:
- Global Supplier
- Lokal Company

### Mahsulotlar (3 ta namuna):
- Non (kod: FOOD001)
- Alik sut (kod: FOOD002)
- Guruch (kod: FOOD003)

## 6. WEB INTERFEYS

### Sahifalar:
1. **Bosh Sahifa** - Ombor statistikasi
   - Jami mahsulotlar
   - Kam qolgan mahsulotlar
   - Tugagan mahsulotlar
   - Oxirgi operatsiyalar

2. **Mahsulotlar** - Barcha mahsulotlarni ko'rish va boshqarish
   - Mahsulot qidirish
   - Kategoriya bo'yicha filtrlash
   - Yangi mahsulot qo'shish
   - Mahsulot yangilash/o'chirish

3. **Qoldiq Hisoboti** - Ombord nik holatini tekshirish
   - Jami mahsulotlar
   - Kam qolgan mahsulotlar ro'yxati
   - Tugagan mahsulotlar

4. **Operatsiyalar** - Kirim/chiqim historiyasi
   - Sanalar bo'yicha filtrlash
   - Operatsiya turini tanlash

## 7. ADMIN PANELI

Admin panelidan:
- Foydalanuvchilarni boshqarish
- Rollari o'zgartirish
- Mahsulotlar ustida to'liq nazorat
- Operatsiyalarni ko'rish
- Notifikatsiyalarni boshqarish

## 8. API ENDPOINTS

Frontend yoki boshqa ilovalardan foydalanish uchun:

```
GET /                     - Bosh sahifa
GET /products/            - Mahsulotlar ro'yxati
GET /products/<id>/       - Mahsulot haqida
POST /products/create/    - Mahsulot qo'shish
POST /products/<id>/transaction/ - Operatsiya qo'shish
GET /reports/stock/       - Qoldiq hisoboti
GET /reports/transactions/ - Operatsiya hisoboti
```

## 9. XATOLARNI TUZATISH

### Database xataligi
```powershell
python manage.py migrate
```

### Static fayllar topilmasa
```powershell
python manage.py collectstatic
```

### Aniq xatolikni ko'rish uchun
1. DEBUG=True .env da bo'lishiga tekshirish
2. Django xato xabarlarini o'qish

## 10. TELEFON/MOBIL UCHUN

Telefon orqali kirilishi uchun:
```powershell
python manage.py runserver 0.0.0.0:8000
```

Keyin kompyuter'niki IP manzil:8000 da kirish (misol: http://192.168.1.100:8000/)

## 11. MUHIM FAYLLAR

- `manage.py` - Django bosh buyruq fayli
- `warehouse/settings.py` - Loyiha sozlamalari
- `inventory/models.py` - Ma'lumotlar modellari
- `inventory/views.py` - Web sahifalari
- `inventory/admin.py` - Admin paneli sozlamasi
- `.env` - Muhit parametrlari
- `db.sqlite3` - Ma'lumotlar bazasi

## 12. DAVOM ETISH

Ushbu loyiha tayyor tuzilmaganga asosan ishlab chiqilgan. Keyin quyidagilarni qo'shish mumkin:

- [ ] Foydalanuvchi avtentifikatsiyasi
- [ ] Ruxsatlar boshqarish
- [ ] PDF hisobotlar
- [ ] Email bildirishnomalar  
- [ ] Advanced analytics
- [ ] Mobile app

## 13. YORDAM VA MUAMMOLAR

Terminal oynasida xatoliklarni diqqat bilan o'qiydi:
- Python xatolari
- Migratsiya muammolari
- Import qilishdagi muammolar

## YO'NAL TARAFLAR

Kuchli javoyi:
1. Admin paneli - admin.py dosyesi orqali
2. Telegram bot - bot/handlers.py orqali  
3. Web interfeysi - templates/ orqali
4. Database - inventory/models.py orqali

---
Yana biror savol bo'lsa, README.md faylini o'qiydi yoki admin panelga kirib ko'ring!
