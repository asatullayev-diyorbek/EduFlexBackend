#!/bin/bash
# EduFlex Backend ishga tushirish
cd "$(dirname "$0")"
venv/bin/python manage.py runserver 8000
