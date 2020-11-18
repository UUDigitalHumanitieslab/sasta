from django.urls import path
from .views import ProcessAllTranscriptsView

urlpatterns = [
    path('process_all', ProcessAllTranscriptsView.as_view())
]
