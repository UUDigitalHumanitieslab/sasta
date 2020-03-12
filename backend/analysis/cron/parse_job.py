import os

from bs4 import BeautifulSoup
from corpus2alpino.annotators.alpino import AlpinoAnnotator
from corpus2alpino.collectors.filesystem import FilesystemCollector
from corpus2alpino.converter import Converter
from corpus2alpino.log import Log, LogSingleton, LogTarget
from corpus2alpino.models import CollectedFile, Document
from corpus2alpino.targets.filesystem import FilesystemTarget
from corpus2alpino.writers.lassy import LassyWriter
from django.core.files import File
from django_cron import CronJobBase, Schedule

from ..models import Transcript, Utterance
from django.db.models import Q


class ParseJob(CronJobBase):
    RUN_EVERY_MINS = 1

    schedule = Schedule(run_every_mins=1)
    code = 'sasta.parse_job'  # a unique code

    def do(self):
        log_target = LogTarget(target=FilesystemTarget(
            'logs'))
        log_target.document = Document(CollectedFile(
            '', 'parse.log', 'text/plain', ''), [])
        LogSingleton.set(Log(log_target, strict=False))

        for transcript in Transcript.objects.filter(Q(status='converted') | Q(status='parsing-failed')):
            try:
                output_path = transcript.content.path.replace(
                    '/transcripts', '/parsed')
                output_dir = os.path.dirname(output_path)
                os.makedirs(output_dir, exist_ok=True)
                self.parse_transcript(transcript, output_dir, output_path)
                self.create_utterance_objects(transcript, output_path)
            except Exception as e:
                LogSingleton.get().error(
                    f'ERROR parsing "{transcript.name}" with message:\t{e}\n')

    def parse_transcript(self, transcript, output_dir, output_path):
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
            with open(output_path, 'rb') as parsed_file_content:
                parsed_filename = os.path.basename(
                    output_path).replace('.cha', '.xml')
                transcript.parsed_content.save(
                    parsed_filename, File(parsed_file_content))

        except Exception as e:
            LogSingleton.get().error(
                f'ERROR parsing "{transcript.name}" with message:\t{e}\n')
            transcript.status = 'parsing-failed'
            transcript.save()

    def create_utterance_objects(self, transcript, parsed_filepath):
        with open(parsed_filepath, 'rb') as f:
            try:
                doc = BeautifulSoup(f.read(), 'xml')
                utts = doc.find_all('alpino_ds')
                num_created = 0
                for utt in utts:
                    xsid = utt.metadata.find(
                        'meta', {'name': 'xsid'})
                    if xsid:
                        utt_id = xsid['value']
                        # replace existing utterances
                        existing = Utterance.objects.filter(
                            transcript=transcript, utt_id=utt_id)
                        if existing:
                            existing.delete()
                        sent = utt.sentence.text
                        speaker = utt.metadata.find(
                            'meta', {'name': 'speaker'})['value']
                        instance = Utterance(
                            transcript=transcript,
                            utt_id=utt_id,
                            speaker=speaker,
                            text=sent
                        )
                        instance.save()
                        num_created += 1
                LogSingleton.get().warning(
                    f'Created {num_created} (out of {len(utts)}) utterances for:\t{transcript.name}\n')

            except Exception as e:
                LogSingleton.get().error(
                    f'ERROR creating utterances for:\t{transcript.name} with message:\t"{e}"\n')
