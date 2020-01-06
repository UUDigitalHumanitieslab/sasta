from django.urls import path, include

from . import views

urlpatterns = [
    path('upload', views.upload),
    path('list', views.list),
    path('convert', views.convert),
    path('delete', views.delete),
]
