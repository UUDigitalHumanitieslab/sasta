import logging

from django.db.models import Q
from django_cron import CronJobBase, Schedule

from ..convert.convert import convert
from ..models import Transcript

logger = logging.getLogger('sasta')


class ConvertJob(CronJobBase):
    RUN_EVERY_MINS = 1

    schedule = Schedule(run_every_mins=1)
    code = 'sasta.convert_job'

    def do(self):
        for transcript in Transcript.objects.filter(
                Q(status='created') | Q(status='conversion-failed')):
            try:
                convert(transcript)
            except Exception as error:
                logger.error(f'error in convert_cron:\t{error}')
