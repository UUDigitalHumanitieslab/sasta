import logging
import os
import os.path as op

from analysis.models import Transcript
from convert.chat_reader import ChatDocument
from convert.chat_writer import ChatWriter

from .chat_converter import SifReader

logger = logging.getLogger('sasta')


def convert(transcript: Transcript):
    transcript.status = Transcript.CONVERTING
    transcript.save()

    try:
        if transcript.content.name.endswith('.txt'):
            reader = SifReader(transcript.content.path)
            cha_name = transcript.content.name.replace('.txt', '.cha')
            cha_path = transcript.content.path.replace('.txt', '.cha')
            # use title from metadata, if present
            title = reader.document.title
            if title:
                cha_name = cha_name.replace(transcript.name, title)
                cha_path = cha_path.replace(transcript.name, title)
                transcript.name = title
            transcript.target_ids = reader.document.target_uttids
            transcript.target_speakers = ','.join(
                reader.document.target_speaker_codes)
            reader.document.write_chat(cha_path)
            # remove the old .txt transcript file
            os.remove(transcript.content.path)
            # set transcript file to .cha file
            transcript.content = cha_name

        elif transcript.content.name.endswith('.cha'):
            doc = ChatDocument.from_chatfile(transcript.content.path, transcript.corpus.method_category)
            transcript.target_ids = doc.target_uttids
            transcript.target_speakers = ','.join(doc.target_speakers)
            transcript.name = op.splitext(
                op.basename(transcript.content.name))[0]

            # overwrite with processed chat
            filename = transcript.content.name
            filepath = transcript.content.path
            transcript.content.delete(False)
            writer = ChatWriter(doc, filename=filepath)
            writer.write()
            transcript.content = filename

        else:
            raise ValueError('Invalid file extension.')

        transcript.status = Transcript.CONVERTED
        transcript.save()
        logger.info('Conversion successful')
        return transcript

    except Exception as e:
        transcript.status = Transcript.CONVERSION_FAILED
        transcript.save()
        logger.exception(e)
        # raise
