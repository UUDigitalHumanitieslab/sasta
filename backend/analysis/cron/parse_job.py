import os

from corpus2alpino.annotators.alpino import AlpinoAnnotator
from corpus2alpino.collectors.filesystem import FilesystemCollector
from corpus2alpino.converter import Converter
from corpus2alpino.log import Log, LogSingleton, LogTarget
from corpus2alpino.targets.filesystem import FilesystemTarget
from corpus2alpino.targets.memory import MemoryTarget
from corpus2alpino.writers.lassy import LassyWriter
from django_cron import CronJobBase, Schedule

from ..models import Transcript


class ParseJob(CronJobBase):
    RUN_EVERY_MINS = 1

    schedule = Schedule(run_every_mins=1)
    code = 'sasta.parse_job'  # a unique code

    def do(self):
        print('Running ParseJob')
        # for transcript in Transcript.objects.filter(name="Stap_01_TranscriptWord"):
        for transcript in Transcript.objects.all():
            try:
                self.parse_transcript(transcript)
            except Exception as e:
                print('klapt op do()')
                print(e)

    def parse_transcript(self, transcript):
        transcript.status = 'parsing'
        transcript.save()

        try:
            transcript_dir, _ = os.path.splitext(transcript.content.path)
            os.makedirs(transcript_dir, exist_ok=True)
            print(transcript.name)

            alpino = AlpinoAnnotator("localhost", 7001)

            # log_singleton = LogSingleton
            # log_target = LogTarget(target=FilesystemTarget(
            #     'logs'))
            # log = Log(log_target, strict=False)
            # log_singleton.set(log)

            converter = Converter(
                collector=FilesystemCollector([transcript.content.path]),
                annotators=[alpino],
                target=FilesystemTarget(transcript_dir),
                # target=MemoryTarget(),
                writer=LassyWriter(False),
            )
            parses = converter.convert()
            for parse in parses:
                print(parse)
            transcript.status = 'parsed'
            transcript.save()
            print('----')

        except Exception as e:
            print('parse klapt')
            print(e)
            transcript.status = 'parsing-failed'
            transcript.save()
