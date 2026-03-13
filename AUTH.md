# 🔐 Autentifikatsiya Tizimi - Do'kon Omborini Boshqarish

## Ro'yxatdan O'tish va Kirish

Do'kon Omborini Boshqarish Tizimida to'liq Django autentifikatsiya tizimi o'rnatilgan. Bu tizim foydalanuvchilarga xavfsiz ro'yxatdan o'tish, kirish va parolni tiklash imkoniyatini beradi.

## 1. Kirish (Login)

### URL
```
http://localhost:8000/login/
```

### Kirish uchun kerak bo'ladi:
- **Foydalanuvchi Nomi**: Ro'yxatdan O'tish paytida kiritilgan
- **Parol**: Yangi parol (8 ta belgi, harf va raqamlar)

### Xususiyatlar:
✅ "Meni Eslab Qol" - Session saqlanib qoladi
✅ "Parolni Unutdingizmi?" - Parol tiklash
✅ Yangi foydalanuvchi ro'yxatdan o'tish

## 2. Ro'yxatdan O'tish (Register)

### URL
```
http://localhost:8000/register/
```

### Kerak bo'ladi:
1. **Foydalanuvchi Nomi** (username)
   - Maximal 30 ta belgi
   - Faqat harflar, raqamlar va @/./+/-/_
   - Unikal (boshqa foydalanuvchi ishlatmagani)

2. **Email Manzil**
   - Haqiqiy email bo'lishi kerak
   - Parolni tiklash uchun zarur

3. **Ismingiz** (ixtiyoriy)
   - Foydalanuvchini to'liq nomidan
   - Admin panelda ko'rinadi

4. **Familiyangiz** (ixtiyoriy)
   - Qo'shimcha ma'lumot

5. **Parol**
   - Kamida 8 ta belgi
   - Harf va raqamlar bo'lishi kerak
   - Xavfsiz parol tanlang

6. **Parolni Tasdiqlash**
   - Parol qayta kiritiladi
   - Ikkala parol mos kelishi kerak

### Ro'yxatdan O'tish jarayoni:
1. Barcha maydonlarni to'ldirish
2. "Ro'yxatdan O'tish" tugmasini bosish
3. Tizim yangi foydalanuvchi yaratadi
4. Avtomatik "Do'kon xodimi" roli tayinlanadi
5. Kirish sahifasiga o'tish

## 3. Parolni Tiklash (Password Reset)

### URL
```
http://localhost:8000/password-reset/
```

### Parol Unutdingiz bo'lsa:

#### 1-bosqich: Email Kiritish
```
http://localhost:8000/password-reset/
```
- Email manzilni kiriting
- "Parol Tiklash Linkini Yuborish" bosing

#### 2-bosqich: Email-da Linkni Ochish
- Email-ni tekshiring (Spam papkani ham tekshiring!)
- Linkni bosing (link 24 soat amal qiladi)

#### 3-bosqich: Yangi Parol Yaratish
```
http://localhost:8000/password-reset/<uid>/<token>/
```
- Yangi parol kiriting
- Parolni tasdiqlang
- "Parolni O'zgaritirish" bosing

#### 4-bosqich: Muvaffaqiyat
- "✅ Muvaffaqiyatli!" sahifasi ko'rinadi
- Yangi parol bilan kirish sahifasiga o'ting

## 4. Chiqish (Logout)

### URL
```
http://localhost:8000/logout/
```

- Navbardan "Chiqish" tugmasini bosing
- Session o'chib ketadi
- Kirish sahifasiga yo'naltiriladi

## 5. Foydalanuvchi Rollari

Ro'yxatdan O'tgandan keyin avtomatik rol tayinlanadi:

### Do'kon xodimi (Staff) - Default
```
✅ Mahsulot qidirish
✅ Qoldiq nazorati
✅ Oddiy operatsiyalar
```

### Omborchi (Warehouseman) - Admin tayinlaydi
```
✅ Kirim/Chiqim operatsiyalari
✅ Ombor boshqaruvi
✅ Statistika ko'rish
```

### Admin - Admin tayinlaydi
```
✅ Tizim to'liq boshqaruvi
✅ Foydalanuvchi boshqaruvi
✅ Hisobotlar va analitika
```

**Rol o'zgaritirish:** Admin paneldan `/admin/`

## 6. Xavfsizlik Xususiyatlari

### Password Xavfsizlik
✅ Kamida 8 ta belgi
✅ Harf va raqamlar zarur
✅ Django password validators
✅ Hashed storage (salted)

### Session Xavfsizlik
✅ CSRF protection
✅ XSS protection
✅ Secure session cookies
✅ Session timeout

### Email Xavfsizlik
✅ Token-based reset
✅ 24-soatlik muddati
✅ One-time link

## 7. Email Sozlash (Production uchun)

### Gmail orqali:

1. Google akkauntida 2-faktor autentifikatsiyani yoqing
2. App Password yaratish:
   - `https://myaccount.google.com/apppasswords` ga o'tish
   - "Mail" va "Windows Computer" tanlang
   - 16-belgili parol oling

3. `.env` faylida:
```
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=xxxxxxxxxxxxxxxx
DEFAULT_FROM_EMAIL=your-email@gmail.com
```

### Boshqa serverlari uchun:
Sendgrid, Mailgun yoki boshqa SMTP serveri ishlatish mumkin

## 8. Test Qilish

### Admin paneli orqali test:
```
http://localhost:8000/admin/
```

1. Admin akkauntini yaratish:
```bash
python manage.py createsuperuser
```

2. Foydalanuvchilarni boshqarish
3. Rollar o'zgartirish
4. Profil ma'lumotlarini tahrir qilish

## 9. Ko'p So'raladigan Savol-Javoblar

**S: Parolni unutdim?**
J: `/password-reset/` ga o'tib, email manzilni kiriting. Email-da link olasiz.

**S: Email-da link olmadim?**
J: 
1. Spam papkani tekshiring
2. Email manzil to'g\'ri kiritilganini tekshiring
3. Console EmailBackend ishlatilayotganini tekshiring (development da)

**S: Akkaunt blockirovka?**
J: Hozircha avtomatik blockiralanmaydi. Admin `/admin/` dan deactivate qilishi mumkin.

**S: Parolni o'zgartirish?**
J: Profil sahifasida yoki `/admin/` panelda

**S: Social login (Google, Facebook)?**
J: `django-allauth` package ishlatib, keyingi versiyada qo'shilishi mumkin

## 10. Migrations va Setup

### Database sozlash:
```bash
# Migratsiyalar oldin bajargan bo'lsa:
python manage.py migrate

# Agar yangi auth views qo'shilgan bo'lsa:
python manage.py makemigrations
python manage.py migrate
```

### Boshlang'ich ma'lumotlar:
```bash
python manage.py init_data  # Kategoriyalar, mahsulotlar va boshqa
python manage.py createsuperuser  # Admin yaratish
```

## 11. Views va URLs

### Authentication URLs:
```python
/login/              - Kirish sahifasi
/register/           - Ro'yxatdan O'tish
/logout/             - Chiqish
/password-reset/     - Parol tiklash so'rash
/password-reset/<uid>/<token>/  - Yangi parol yaratish
/password-reset/done/            - Tugallanish
```

### Protected Views (Login Kerak):
```python
/                    - Bosh sahifa (Dashboard)
/products/           - Mahsulotlar
/reports/stock/      - Qoldiq hisoboti
/reports/transactions/ - Operatsiya hisoboti
```

## 12. Kengaytirish Imkoniyatlari

- [ ] Two-Factor Authentication (2FA)
- [ ] Social Login (Google, Facebook)
- [ ] Email Verification
- [ ] Account Lockout
- [ ] Login History
- [ ] API Token Authentication
- [ ] OAuth 2.0

---

**E'tibor:** Production-da:
- `DEBUG=False` o'rnatish
- `SECRET_KEY` o'zgartirish
- HTTPS ishlatish
- Email serverni sozlash
- Session timeout o'zgartirish
