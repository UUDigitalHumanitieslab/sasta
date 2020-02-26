import os

from corpus2alpino.annotators.alpino import AlpinoAnnotator
from corpus2alpino.collectors.filesystem import FilesystemCollector
from corpus2alpino.converter import Converter
from corpus2alpino.log import Log, LogSingleton, LogTarget
from corpus2alpino.targets.filesystem import FilesystemTarget
from corpus2alpino.writers.lassy import LassyWriter
from django_cron import CronJobBase, Schedule

from ..models import Transcript

from lxml import etree
from bs4 import BeautifulSoup


class ParseJob(CronJobBase):
    RUN_EVERY_MINS = 1

    schedule = Schedule(run_every_mins=1)
    code = 'sasta.parse_job'  # a unique code

    def do(self):
        LogSingleton.set(Log(LogTarget(target=FilesystemTarget(
            'logs')), strict=False))

        # for transcript in Transcript.objects.filter(status='converted'):
        for transcript in Transcript.objects.all()[:3]:
            try:
                output_path = transcript.content.path.replace(
                    '/transcripts', '/parsed')
                output_dir = os.path.dirname(output_path)
                os.makedirs(output_dir, exist_ok=True)
                # self.parse_transcript(transcript, output_dir)
                self.create_utterance_objects(output_path)
            except Exception as e:
                print(e)
                LogSingleton.get().error(
                    f'Error parsing "{transcript.name}" with message:\t{e}\n')

    def parse_transcript(self, transcript, output_dir):
        transcript.status = 'parsing'
        transcript.save()

        try:
            LogSingleton.get().warning(f'Parsing:\t{transcript.name}\n')

            alpino = AlpinoAnnotator("localhost", 7001)

            converter = Converter(
                collector=FilesystemCollector([transcript.content.path]),
                annotators=[alpino],
                target=FilesystemTarget(output_dir),
                writer=LassyWriter(merge_treebanks=True),
            )
            parses = converter.convert()
            for _parse in parses:
                LogSingleton.get().warning(
                    f'Succesfully parsed:\t{transcript.name}\n')
            transcript.status = 'parsed'
            transcript.save()

        except Exception as e:
            LogSingleton.get().error(
                f'Error parsing "{transcript.name}" with message:\t{e}\n')
            transcript.status = 'parsing-failed'
            transcript.save()

    def create_utterance_objects(self, parsed_filepath):
        with open(parsed_filepath, 'rb') as f:
            try:
                doc = BeautifulSoup(f.read(), 'xml')
                utts = doc.find_all('alpino_ds')
                for utt in utts:
                    print(utt.sentence.text)

            except Exception as e:
                #TODO: log
                print(e)
