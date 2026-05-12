def is_admin(request):
    return request.user.is_active and request.user.role == 'admin'
