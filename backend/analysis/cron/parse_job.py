from ..parse.parse import create_utterance_objects, parse_transcript
from ..models import Transcript
from django_cron import CronJobBase, Schedule
from django.db.models import Q
from corpus2alpino.targets.filesystem import FilesystemTarget
from corpus2alpino.models import CollectedFile, Document
import logging
import os

<< << << < HEAD
== == == =
>>>>>> > develop


logger = logging.getLogger('sasta')


class ParseJob(CronJobBase):
    RUN_EVERY_MINS = 1

    schedule = Schedule(run_every_mins=1)
    code = 'sasta.parse_job'  # a unique code

    def do(self):
        for transcript in Transcript.objects.filter(
                Q(status='converted') | Q(status='parsing-failed')):
            try:
                output_path = transcript.content.path.replace(
                    '/transcripts', '/parsed')
                output_dir = os.path.dirname(output_path)
                os.makedirs(output_dir, exist_ok=True)
                parse_transcript(transcript, output_dir, output_path)
                create_utterance_objects(transcript)
            except Exception:
                logger.exception(f'ERROR parsing {transcript.name}')
