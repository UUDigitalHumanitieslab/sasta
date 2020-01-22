from ..models import Transcript
from django_cron import CronJobBase, Schedule
from corpus2alpino.converter import Converter
from corpus2alpino.annotators.alpino import AlpinoAnnotator
from corpus2alpino.collectors.filesystem import FilesystemCollector
from corpus2alpino.targets.memory import MemoryTarget
from corpus2alpino.writers.lassy import LassyWriter


class ParseJob(CronJobBase):
    RUN_EVERY_MINS = 1

    schedule = Schedule(run_every_mins=1)
    code = 'sasta.parse_job'  # a unique code

    def do(self):
        print('Running ParseJob')
        for transcript in Transcript.objects.all():
            print(transcript.content.path)
            alpino = AlpinoAnnotator("localhost", 7001)
            converter = Converter(
                collector=FilesystemCollector([transcript.content.path]),
                annotators=[alpino],
                target=MemoryTarget(),
                writer=LassyWriter(True)
            )
            parses = converter.convert()
            print(''.join(parses))
            break
