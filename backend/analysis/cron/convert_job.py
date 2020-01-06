from django_cron import CronJobBase, Schedule
from ..models import Transcript
from ..convert.chat_converter import SifReader
import os


class ConvertJob(CronJobBase):
    RUN_EVERY_MINS = 1

    schedule = Schedule(run_every_mins=1)
    code = 'sasta.convert_job'

    def do(self):
        for transcript in Transcript.objects.filter(status='created'):
            try:
                self.convert(transcript)
            except Exception as error:
                print(error)
        # pass

    def convert(self, transcript):
        transcript.status = 'converting'
        transcript.save()

        try:
            cha_path = transcript.content.name.replace('.txt', '.cha')
            reader = SifReader(transcript.content.name)
            reader.document.write_chat(cha_path)

            os.remove(transcript.content.name)
            transcript.content = cha_path
            transcript.status = 'converted'
            transcript.save()

        except:
            transcript.status = 'conversion-failed'
            transcript.save()
            raise
