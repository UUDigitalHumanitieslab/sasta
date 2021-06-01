import os
import logging
from .chat_converter import SifReader

logger = logging.getLogger('sasta')


def convert(transcript):
    transcript.status = 'converting'
    transcript.save()

    try:
        reader = SifReader(transcript.content.path)
        cha_name = transcript.content.name.replace('.txt', '.cha')
        cha_path = transcript.content.path.replace('.txt', '.cha')
        # use title from metadata, if present
        title = reader.document.title
        if title:
            cha_name = cha_name.replace(transcript.name, title)
            cha_path = cha_path.replace(transcript.name, title)
            transcript.name = title
        reader.document.write_chat(cha_path)
        # remove the old .txt transcript file
        os.remove(transcript.content.path)
        # set transcript file to .cha file
        transcript.content = cha_name
        transcript.status = 'converted'
        transcript.save()
        logger.info('Conversion successful')
        return transcript

    except Exception:
        transcript.status = 'conversion-failed'
        transcript.save()
        logger.warn('Conversion failed')
        # raise
