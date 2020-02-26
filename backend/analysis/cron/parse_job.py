import os

from corpus2alpino.annotators.alpino import AlpinoAnnotator
from corpus2alpino.collectors.filesystem import FilesystemCollector
from corpus2alpino.converter import Converter
from corpus2alpino.log import Log, LogSingleton, LogTarget
from corpus2alpino.targets.filesystem import FilesystemTarget
from corpus2alpino.writers.lassy import LassyWriter
from django_cron import CronJobBase, Schedule

from ..models import Transcript


class ParseJob(CronJobBase):
    RUN_EVERY_MINS = 1

    schedule = Schedule(run_every_mins=1)
    code = 'sasta.parse_job'  # a unique code

    def do(self):
        LogSingleton.set(Log(LogTarget(target=FilesystemTarget(
            'logs')), strict=True))

        for transcript in Transcript.objects.filter(status='converted'):
            try:
                self.parse_transcript(transcript)
            except Exception as e:
                print('klapt op do()')
                print(e)

    def parse_transcript(self, transcript):
        transcript.status = 'parsing'
        transcript.save()

        try:
            LogSingleton.get().warning(f'Parsing:\t{transcript.name}\n')
            transcript_dir, _ = os.path.splitext(transcript.content.path)
            os.makedirs(transcript_dir, exist_ok=True)

            alpino = AlpinoAnnotator("localhost", 7001)

            converter = Converter(
                collector=FilesystemCollector([transcript.content.path]),
                annotators=[alpino],
                target=FilesystemTarget(transcript_dir),
                writer=LassyWriter(False),
            )
            parses = converter.convert()
            for _parse in parses:
                LogSingleton.get().warning(
                    f'Succesfully parsed:\t{transcript.name}')
            transcript.status = 'parsed'
            transcript.save()

        except Exception as e:
            LogSingleton.get().error(
                f'Error parsing "{transcript.name}" with message:\t{e}')
            transcript.status = 'parsing-failed'
            transcript.save()
