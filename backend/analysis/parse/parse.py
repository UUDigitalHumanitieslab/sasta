import logging
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
from django.db.models import Q

from ..models import Transcript, Utterance

logger = logging.getLogger('sasta')


def parse_and_create(transcript):
    log_target = LogTarget(target=FilesystemTarget(
        'logs'))
    log_target.document = Document(CollectedFile(
        '', 'parse.log', 'text/plain', ''), [])
    LogSingleton.set(Log(log_target, strict=False))

    try:
        output_path = transcript.content.path.replace(
            '/transcripts', '/parsed')
        output_dir = os.path.dirname(output_path)
        os.makedirs(output_dir, exist_ok=True)
        result = parse_transcript(transcript, output_dir, output_path)
        create_utterance_objects(transcript)
        return result
    except Exception as e:
        logger.exception(f'ERROR parsing {transcript.name}')


def parse_transcript(transcript, output_dir, output_path):
    transcript.status = 'parsing'
    transcript.save()

    try:
        logger.info(f'Parsing:\t{transcript.name}\n')

        alpino = AlpinoAnnotator("127.0.0.1", 7001)

        converter = Converter(
            collector=FilesystemCollector([transcript.content.path]),
            annotators=[alpino],
            target=FilesystemTarget(output_dir),
            writer=LassyWriter(merge_treebanks=True),
        )
        parses = converter.convert()
        for _parse in parses:
            logger.info(f'Succesfully parsed:\t{transcript.name}\n')
        transcript.status = 'parsed'
        transcript.save()
        parsed_file_content = open(output_path, 'rb')
        parsed_filename = os.path.basename(
            output_path).replace('.cha', '.xml')
        transcript.parsed_content.save(
            parsed_filename, File(parsed_file_content))
        os.remove(output_path)
        return transcript

    except Exception as e:
        logger.exception(
            f'ERROR parsing {transcript.name}')
        transcript.status = 'parsing-failed'
        transcript.save()


def create_utterance_objects(transcript):
    with open(transcript.parsed_content.path, 'rb') as f:
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
                        sentence=sent,
                        parse_tree=str(utt)
                    )
                    instance.save()
                    num_created += 1
            logger.info(
                f'Created {num_created} (out of {len(utts)}) utterances for:\t{transcript.name}\n')

        except Exception as e:
            logger.exception(
                f'ERROR creating utterances for:\t{transcript.name} with message:\t"{e}"\n')
