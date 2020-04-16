import logging

from django_cron import CronJobBase, Schedule

from ..models import UploadFile
from ..utils import extract

logger = logging.getLogger('sasta')


class ExtractJob(CronJobBase):
    RUN_EVERY_MINS = 1

    schedule = Schedule(run_every_mins=1)
    code = 'sasta.extract_job'  # a unique code

    def do(self):
        for file in UploadFile.objects.filter(status="pending"):
            try:
                extract(file)
            except Exception as error:
                logger.exception(error)
