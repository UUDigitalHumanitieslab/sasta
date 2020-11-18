from sasta import celery_app as app
from celery import shared_task
from analysis.models import Transcript


@app.task
def add(x, y):
    return x + y


@shared_task
def test_model(model_id):
    obj = Transcript.objects.get(pk=model_id)
    return obj.name
