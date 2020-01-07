import os
from django_cron import CronJobBase, Schedule
from ..convert.chat_converter import SifReader
from ..models import Transcript


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

    def convert(self, transcript):
        transcript.status = 'converting'
        transcript.save()

        try:
            cha_name = transcript.content.name.replace('.txt', '.cha')
            cha_path = transcript.content.path.replace('.txt', '.cha')
            reader = SifReader(transcript.content.path)
            reader.document.write_chat(cha_path)

            # remove the old .txt transcript file
            os.remove(transcript.content.path)

            # set transcript file to .cha file
            transcript.content = cha_name
            transcript.status = 'converted'
            transcript.save()

        except:
            transcript.status = 'conversion-failed'
            transcript.save()
            raise
