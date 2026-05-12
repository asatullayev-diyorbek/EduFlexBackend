# EduFlex — Backend

Django + Django REST Framework asosida qurilgan interaktiv ta'lim platformasi uchun backend API.

## Texnologiyalar

| Texnologiya | Versiya |
|------------|---------|
| Python | 3.11+ |
| Django | 6.0 |
| Django REST Framework | 3.17 |
| SimpleJWT | 5.5 |
| django-cors-headers | 4.9 |

## O'rnatish

### 1. Repozitoriyni klonlash

```bash
git clone <repo-url>
cd backend
```

### 2. Virtual muhit yaratish va faollashtirish

```bash
python -m venv venv
source venv/bin/activate       # Linux/Mac
# venv\Scripts\activate        # Windows
```

### 3. Bog'liqliklarni o'rnatish

```bash
pip install -r requirements.txt
```

### 4. Muhit o'zgaruvchilarini sozlash

```bash
cp .env.example .env
# .env faylini tahrirlang va SECRET_KEY ni o'zgartiring
```

### 5. Ma'lumotlar bazasini tayyorlash

```bash
python manage.py migrate
```

### 6. Demo ma'lumotlar yuklash (ixtiyoriy)

```bash
python seed.py
```

Bu quyidagi demo foydalanuvchilarni yaratadi:

| Email | Parol | Rol |
|-------|-------|-----|
| admin@eduflix.com | admin123 | Admin |
| teacher@eduflix.com | teacher123 | O'qituvchi |
| student@eduflix.com | student123 | Talaba |

### 7. Serverni ishga tushirish

```bash
python manage.py runserver
# yoki
bash run.sh
```

API `http://localhost:8000/api/` manzilida ishlaydi.

---

## API endpointlar

### Autentifikatsiya (`/api/auth/`)

| Method | Endpoint | Tavsif |
|--------|----------|--------|
| POST | `/auth/login/` | Kirish (token olish) |
| POST | `/auth/register/` | Ro'yxatdan o'tish |
| POST | `/auth/logout/` | Chiqish (token blacklist) |
| POST | `/auth/token/refresh/` | Token yangilash |
| GET/PATCH | `/auth/me/` | Joriy foydalanuvchi |
| POST | `/auth/change-password/` | Parol o'zgartirish |

### Testlar (`/api/tests/`)

| Method | Endpoint | Tavsif |
|--------|----------|--------|
| GET/POST | `/tests/` | Testlar ro'yxati / yaratish |
| GET/PATCH/DELETE | `/tests/:id/` | Test detail |
| GET/POST | `/tests/:id/questions/` | Savollar |
| PATCH/DELETE | `/questions/:id/` | Savol detail |
| POST | `/tests/:id/attempts/` | Test boshlash |
| POST | `/attempts/:id/answer/` | Javob yuborish |
| POST | `/attempts/:id/finish/` | Testni yakunlash |
| GET | `/attempts/` | Urinishlar tarixi |
| GET | `/attempts/:id/` | Urinish natijasi |

### Topshiriqlar (`/api/assignments/`)

| Method | Endpoint | Tavsif |
|--------|----------|--------|
| GET/POST | `/assignments/` | Ro'yxat / yaratish |
| GET/PATCH/DELETE | `/assignments/:id/` | Detail |
| POST | `/assignments/:id/publish/` | Nashr toggle |
| POST | `/assignments/:id/start/` | Boshlash (talaba) |
| POST | `/assignments/:id/save/` | Qoralama saqlash |
| POST | `/assignments/:id/submit/` | Yuborish |
| GET | `/assignments/:id/my-submission/` | O'z natijasi |
| GET | `/assignments/:id/submissions/` | Barcha javoblar (o'qituvchi) |
| GET | `/submissions/:id/` | Javob detali |
| POST | `/submissions/:id/grade/` | Baholash |

### Analitika (`/api/analytics/`)

| Method | Endpoint | Tavsif |
|--------|----------|--------|
| GET | `/analytics/dashboard/` | Admin statistika |
| GET | `/analytics/teacher/` | O'qituvchi statistika |
| GET | `/analytics/student/` | Talaba statistika |
| GET | `/analytics/tests/:id/` | Test analitikasi |

### Admin (`/api/admin/`)

| Method | Endpoint | Tavsif |
|--------|----------|--------|
| GET | `/admin/users/` | Foydalanuvchilar ro'yxati |
| GET/PATCH | `/admin/users/:id/` | Foydalanuvchi detail |

---

## Loyiha tuzilmasi

```
backend/
├── config/          # Django sozlamalari, URL lar
├── users/           # Foydalanuvchi modeli, auth
├── tests_app/       # Test, savol, urinish modellari
├── analytics/       # Statistika endpointlar
├── assignments/     # Topshiriq tizimi
├── manage.py
├── seed.py          # Demo ma'lumotlar
├── requirements.txt
├── run.sh
└── .env.example
```

## Litsenziya

BMI (Biznes va IT) loyihasi uchun yaratilgan.
