import logging
import os

from bs4 import BeautifulSoup
from corpus2alpino.annotators.alpino import AlpinoAnnotator
from corpus2alpino.collectors.filesystem import FilesystemCollector
from corpus2alpino.converter import Converter
from corpus2alpino.targets.filesystem import FilesystemTarget
from corpus2alpino.writers.lassy import LassyWriter
from django.core.files import File

from ..models import Utterance

logger = logging.getLogger('sasta')


def parse_transcript(transcript, output_dir, output_path):
    transcript.status = 'parsing'
    transcript.save()

    try:
        logger.info(f'Parsing:\t{transcript.name}\n')

        alpino = AlpinoAnnotator("localhost", 7001)

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
        with open(output_path, 'rb') as parsed_file_content:
            parsed_filename = os.path.basename(
                output_path).replace('.cha', '.xml')
            transcript.parsed_content.save(
                parsed_filename, File(parsed_file_content))

    except Exception as e:
        logger.exception(
            f'ERROR parsing {transcript.name}')
        transcript.status = 'parsing-failed'
        transcript.save()


def create_utterance_objects(transcript, parsed_filepath):
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
