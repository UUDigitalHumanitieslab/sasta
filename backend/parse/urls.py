from django.urls import re_path, path
from .views import ParseTaskView

urlpatterns = [
    path('task/<uuid:task_id>/',
         ParseTaskView.as_view(), name='parse_task_id'),
    path('task/', ParseTaskView.as_view(), name='parse_task')
]
