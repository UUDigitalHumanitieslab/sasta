from django.urls import include, path

from .views import info_from_confirm_key

urlpatterns = [
    path('infofromkey/<key>/', info_from_confirm_key),
    path('', include('rest_auth.urls')),
    path('registration/', include('rest_auth.registration.urls')),
]
