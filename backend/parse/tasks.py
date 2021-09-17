from analysis.models import Corpus, Transcript
from celery import shared_task
from django.db.models import Q

from .parse_utils import parse_and_create


@shared_task
def parse_corpus(corpus_id: int):
    # with connection.cursor as cursor:
    corpus = Corpus.objects.get(pk=corpus_id)
    transcripts = Transcript.objects.filter(Q(corpus=corpus), Q(status=Transcript.CONVERTED) | Q(status=Transcript.PARSING_FAILED))

    succes = 0

    for t in transcripts:
        parsed = parse_and_create(t)
        if not parsed:
            # raise Exception('Parsing failed for %s' % t.name)
            pass
        else:
            succes += 1

    return f'{succes} out of {len(transcripts)} parsed'
