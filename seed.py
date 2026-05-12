"""Seed demo data: users + 2 tests with questions."""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from users.models import User
from tests_app.models import Test, Question

# Users
admin = User.objects.create_user(
    email='admin@eduflix.com', password='admin123',
    name='Admin User', role='admin', is_staff=True, is_superuser=True,
)
teacher = User.objects.create_user(
    email='teacher@eduflix.com', password='teacher123',
    name='John Teacher', role='teacher',
)
student = User.objects.create_user(
    email='student@eduflix.com', password='student123',
    name='Jane Student', role='student',
)

# Extra students
for i in range(1, 6):
    User.objects.create_user(
        email=f'student{i}@eduflix.com', password='student123',
        name=f'Student {i}', role='student',
    )

# Test 1 — JavaScript Basics
test1 = Test.objects.create(
    title='JavaScript Asoslari',
    description="JavaScript dasturlash tilining asosiy tushunchalari bo'yicha test.",
    created_by=teacher,
    time_limit=30,
    is_active=True,
    show_feedback=True,
)

Question.objects.create(
    test=test1, order_index=1, type='multiple_choice', difficulty='easy', points=1,
    text='JavaScript-da o\'zgaruvchi e\'lon qilish uchun qaysi kalit so\'z ishlatiladi?',
    data={
        'options': [
            {'id': 1, 'text': 'var'},
            {'id': 2, 'text': 'let'},
            {'id': 3, 'text': 'const'},
            {'id': 4, 'text': 'Barchasi to\'g\'ri'},
        ],
        'correct': 4,
    },
    explanation='JavaScript-da var, let va const kalit so\'zlari bilan o\'zgaruvchi yaratish mumkin.',
)

Question.objects.create(
    test=test1, order_index=2, type='true_false', difficulty='easy', points=1,
    text='JavaScript ob\'ekt-yo\'naltirilgan dasturlash tili hisoblanadi.',
    data={'correct': True},
    explanation='Ha, JavaScript ob\'ekt-yo\'naltirilgan paradigmani qo\'llab-quvvatlaydi.',
)

Question.objects.create(
    test=test1, order_index=3, type='multiple_choice', difficulty='medium', points=2,
    text='Quyidagilardan qaysi biri JavaScript-da "undefined" qiymat qaytaradi?',
    data={
        'options': [
            {'id': 1, 'text': 'null'},
            {'id': 2, 'text': 'e\'lon qilingan lekin qiymat berilmagan o\'zgaruvchi'},
            {'id': 3, 'text': '0'},
            {'id': 4, 'text': '""'},
        ],
        'correct': 2,
    },
)

Question.objects.create(
    test=test1, order_index=4, type='fill_blank', difficulty='medium', points=2,
    text='JavaScript-da massiv uzunligini olish uchun ___ xususiyati ishlatiladi.',
    data={
        'template': 'JavaScript-da massiv uzunligini olish uchun [blank_1] xususiyati ishlatiladi.',
        'answers': {'blank_1': 'length'},
    },
)

Question.objects.create(
    test=test1, order_index=5, type='matching', difficulty='hard', points=3,
    text='Array metodlarini ularning vazifasi bilan moslang:',
    data={
        'left': [
            {'id': 'a', 'text': 'push()'},
            {'id': 'b', 'text': 'pop()'},
            {'id': 'c', 'text': 'shift()'},
        ],
        'right': [
            {'id': '1', 'text': 'Boshidan element olib tashlaydi'},
            {'id': '2', 'text': 'Oxiriga element qo\'shadi'},
            {'id': '3', 'text': 'Oxiridan element olib tashlaydi'},
        ],
        'pairs': {'a': '2', 'b': '3', 'c': '1'},
    },
)

# Test 2 — Python
test2 = Test.objects.create(
    title='Python Dasturlash',
    description="Python dasturlash asoslari bo'yicha savol va javoblar.",
    created_by=teacher,
    time_limit=20,
    is_active=True,
    show_feedback=True,
)

Question.objects.create(
    test=test2, order_index=1, type='multiple_choice', difficulty='easy', points=1,
    text='Python-da ro\'yxat (list) e\'lon qilish uchun qaysi belgilar ishlatiladi?',
    data={
        'options': [
            {'id': 1, 'text': '{}'},
            {'id': 2, 'text': '[]'},
            {'id': 3, 'text': '()'},
            {'id': 4, 'text': '<>'},
        ],
        'correct': 2,
    },
)

Question.objects.create(
    test=test2, order_index=2, type='true_false', difficulty='easy', points=1,
    text='Python dasturlash tilida ";" bilan qatorni yakunlash shart.',
    data={'correct': False},
    explanation='Python-da qatorni yakunlash uchun ";" kerak emas, yangi qator yetarli.',
)

Question.objects.create(
    test=test2, order_index=3, type='ordering', difficulty='medium', points=2,
    text='Quyidagi Python o\'rganish bosqichlarini to\'g\'ri tartibda joylashtiring:',
    data={
        'items': [
            {'id': 'a', 'text': 'O\'zgaruvchilar va turlar'},
            {'id': 'b', 'text': 'Funksiyalar'},
            {'id': 'c', 'text': 'Sintaksis asoslari'},
            {'id': 'd', 'text': 'OOP'},
        ],
        'correct_order': ['c', 'a', 'b', 'd'],
    },
)

Question.objects.create(
    test=test2, order_index=4, type='poll', difficulty='easy', points=0,
    text='Python-ni qaysi maqsad uchun o\'rganmoqchisiz?',
    data={
        'options': [
            {'id': 1, 'text': 'Ma\'lumotlar tahlili'},
            {'id': 2, 'text': 'Web dasturlash'},
            {'id': 3, 'text': 'Avtomatlashtirish'},
            {'id': 4, 'text': 'Sun\'iy intellekt'},
        ],
    },
)

print('✅ Seed data created successfully!')
print(f'   Users: {User.objects.count()}')
print(f'   Tests: {Test.objects.count()}')
print(f'   Questions: {Question.objects.count()}')
