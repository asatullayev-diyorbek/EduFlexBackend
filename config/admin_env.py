from django.conf import settings


def admin_env(request):
    return "Development" if settings.DEBUG else "Production"
