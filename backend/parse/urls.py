from django.urls import re_path, path
from .views import ParseTaskView

urlpatterns = [
    path('parsetask/<int:task_id>/', ParseTaskView.as_view(), name='parse_task_id'),
    path('parsetask/', ParseTaskView.as_view(), name='parse_task')
    # re_path(r'parsetask/(?:(?P<task_id>\d+)/)?$',
    #         ParseTaskView.as_view(), name='parse_task')
]
