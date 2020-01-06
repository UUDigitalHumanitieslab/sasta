from django_cron import CronJobBase, Schedule
from ..models import Transcript


class ExtractJob(CronJobBase):
    RUN_EVERY_MINS = 1

    schedule = Schedule(run_every_mins=1)
    code = 'sasta.convert_job'

    def do(self):
        for transcript in Transcript.objects.filter(status='created'):
            try:
                self.convert(transcript.content)
            except Exception as error:
                print(error)

    def convert(self, file):
        pass
