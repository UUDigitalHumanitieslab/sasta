import os
from django_cron import CronJobBase, Schedule
from ..convert.chat_converter import SifReader
from ..models import Transcript
from django.db.models import Q
import traceback


class ConvertJob(CronJobBase):
    RUN_EVERY_MINS = 1

    schedule = Schedule(run_every_mins=1)
    code = 'sasta.convert_job'

    def do(self):
        for transcript in Transcript.objects.filter(Q(status='created') | Q(status='conversion-failed')):
            try:
                self.convert(transcript)
            except Exception as error:
                print('error in convert_cron:\t', error)
                print(traceback.format_exc())

    def convert(self, transcript):
        transcript.status = 'converting'
        transcript.save()

        try:
            reader = SifReader(transcript.content.path)
            cha_name = transcript.content.name.replace('.txt', '.cha')
            cha_path = transcript.content.path.replace('.txt', '.cha')
            # use title from metadata, if present
            title = reader.document.title
            if title:
                cha_name = cha_name.replace(transcript.name, title)
                cha_path = cha_path.replace(transcript.name, title)
                transcript.name = title
            reader.document.write_chat(cha_path)
            # remove the old .txt transcript file
            os.remove(transcript.content.path)
            # set transcript file to .cha file
            transcript.content = cha_name
            transcript.status = 'converted'
            transcript.save()

        except Exception as e:
            transcript.status = 'conversion-failed'
            transcript.save()
            raise
