from django.urls import include, path

from .views import info_from_confirm_key, has_admin_access

urlpatterns = [
    path('infofromkey/<key>/', info_from_confirm_key),
    path('', include('rest_auth.urls')),
    path('registration/', include('rest_auth.registration.urls')),
    path('has_admin_access/', has_admin_access),
]
