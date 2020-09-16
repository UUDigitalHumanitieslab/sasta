import logging
import os

from corpus2alpino.log import Log, LogSingleton, LogTarget
from corpus2alpino.models import CollectedFile, Document
from corpus2alpino.targets.filesystem import FilesystemTarget
from django.db.models import Q
from django_cron import CronJobBase, Schedule

from ..models import Transcript
from ..parse.parse import create_utterance_objects, parse_transcript

logger = logging.getLogger('sasta')


class ParseJob(CronJobBase):
    RUN_EVERY_MINS = 1

    schedule = Schedule(run_every_mins=1)
    code = 'sasta.parse_job'  # a unique code

    def do(self):
        log_target = LogTarget(target=FilesystemTarget(
            '.logs'))
        log_target.document = Document(CollectedFile(
            '', 'parse.log', 'text/plain', ''), [])
        LogSingleton.set(Log(log_target, strict=False))

        for transcript in Transcript.objects.filter(Q(status='converted') | Q(status='parsing-failed')):  # noqa: E501
            try:
                output_path = transcript.content.path.replace(
                    '/transcripts', '/parsed')
                output_dir = os.path.dirname(output_path)
                os.makedirs(output_dir, exist_ok=True)
                parse_transcript(transcript, output_dir, output_path)
                create_utterance_objects(transcript)
            except Exception:
                logger.exception(f'ERROR parsing {transcript.name}')
