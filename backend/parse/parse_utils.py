import io
import logging
import os

from analysis.models import Transcript, Utterance
from bs4 import BeautifulSoup
from corpus2alpino.annotators.alpino import AlpinoAnnotator
from corpus2alpino.collectors.filesystem import FilesystemCollector
from corpus2alpino.converter import Converter
from corpus2alpino.targets.filesystem import FilesystemTarget
from corpus2alpino.writers.lassy import LassyWriter
from django.conf import settings
from django.core.files import File
from lxml import etree
from sastadev.correcttreebank import correcttreebank, corrn
from sastadev.targets import get_targets

logger = logging.getLogger('sasta')


def parse_and_create(transcript):
    try:
        output_path = transcript.content.path.replace(
            '/transcripts', '/parsed')
        output_dir = os.path.dirname(output_path)
        os.makedirs(output_dir, exist_ok=True)
        result = parse_transcript(transcript, output_dir, output_path)
        create_utterance_objects(transcript)
        return result
    except Exception:
        logger.exception(f'ERROR parsing {transcript.name}')


def parse_transcript(transcript, output_dir, output_path):
    transcript.status = Transcript.PARSING
    transcript.save()

    try:
        logger.info(f'Parsing:\t{transcript.name}...\n')

        # Parser setup
        alpino = AlpinoAnnotator(
            settings.ALPINO_HOST,
            settings.ALPINO_PORT
        )

        converter = Converter(
            collector=FilesystemCollector([transcript.content.path]),
            annotators=[alpino],
            target=FilesystemTarget(output_dir),
            writer=LassyWriter(merge_treebanks=True),
        )

        # Alpino parsing
        parses = converter.convert()
        for _parse in parses:
            logger.info(f'Succesfully parsed:\t{transcript.name}\n')
        transcript.status = Transcript.PARSED
        transcript.save()

        # Saving parsed file
        parsed_file_content = open(output_path, 'rb')
        parsed_filename = os.path.basename(
            output_path).replace('.cha', '.xml')
        transcript.parsed_content.save(
            parsed_filename, File(parsed_file_content))
        os.remove(output_path)

        # Correcting and reparsing
        logger.info(f'Correcting:\t{transcript.name}...\n')
        try:
            corrected, error_dict, _origandalts = correct_treebank(transcript)
            corrected_content = etree.tostring(corrected, encoding='utf-8')
            corrected_filename = parsed_filename.replace('.xml', '_corrected.xml')
            corrected_file = File(io.BytesIO(corrected_content))
            transcript.corrected_content.save(corrected_filename, corrected_file)
            logger.info(f'Successfully corrected:\t{transcript.name}, {len(error_dict)} corrections.\n')
            # Save corrections
            transcript.corrections = error_dict

        except Exception as err:
            transcript.corrections = {'error': str(err)}
            logger.warning(f'Correction failed for transcript:\t {transcript.name}')

        transcript.save()
        return transcript

    except Exception:
        logger.exception(
            f'ERROR parsing {transcript.name}')
        transcript.status = Transcript.PARSING_FAILED
        transcript.save()


def create_utterance_objects(transcript):
    parse_file = transcript.corrected_content or transcript.parsed_content

    with open(parse_file.path, 'rb') as f:
        try:
            marked_utt_counter = 1
            doc = BeautifulSoup(f.read(), 'xml')
            utts = doc.find_all('alpino_ds')
            num_created = 0
            for utt in utts:
                uttno_el = utt.metadata.find(
                    'meta', {'name': 'uttno'}
                )
                uttno = int(uttno_el['value'])

                # replace existing utterances
                existing = Utterance.objects.filter(
                    transcript=transcript, uttno=uttno)
                if existing:
                    existing.delete()
                    logger.info(f'Deleting existing utterance {uttno}')

                sent = utt.sentence.text
                speaker = utt.metadata.find(
                    'meta', {'name': 'speaker'})['value']

                xsid_el = utt.metadata.find(
                    'meta', {'name': 'xsid'})

                # fields that should always be present
                instance = Utterance(
                    transcript=transcript,
                    uttno=uttno,
                    xsid=int(xsid_el['value']) if xsid_el is not None else None,
                    speaker=speaker,
                    sentence=sent,
                    parse_tree=str(utt)
                )

                if instance.for_analysis:
                    # setting utt_id according to targets
                    if transcript.target_ids:
                        # check if xsids are unique and consecutive
                        assert instance.xsid == marked_utt_counter
                    instance.utt_id = marked_utt_counter
                    marked_utt_counter += 1

                instance.save()
                num_created += 1
            logger.info(
                f'Created {num_created} (out of {len(utts)})'
                f'utterances for:\t{transcript.name}\n')

        except Exception as e:
            logger.exception(
                f'ERROR creating utterances for:\t{transcript.name}'
                f'with message:\t"{e}"\n')


def correct_treebank(transcript: Transcript):
    try:
        treebank = etree.parse(transcript.parsed_content).getroot()
        targets = get_targets(treebank)
        method_name = transcript.corpus.method_category.name.lower()

        corr, error_dict, origandalts = correcttreebank(treebank, targets, method_name, corrn)

        return corr, error_dict, origandalts

    except Exception as e:
        logger.exception(e)
        raise
