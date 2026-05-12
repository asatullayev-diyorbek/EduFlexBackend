from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('django-admin/', admin.site.urls),
    path('api/', include('users.urls')),
    path('api/', include('tests_app.urls')),
    path('api/', include('analytics.urls')),
    path('api/', include('assignments.urls')),
]
