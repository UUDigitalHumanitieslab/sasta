import os
import logging

from analysis.models import Transcript
from .chat_converter import SifReader
from convert.chat_reader import ChatDocument

logger = logging.getLogger('sasta')


def convert(transcript: Transcript):
    transcript.status = 'converting'
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
            print('a')
            doc = ChatDocument.from_chatfile(transcript.content.path)
            print('b')
            transcript.target_ids = doc.target_uttids
            print('c')
            transcript.target_speakers = ','.join(doc.target_speakers)
            print('d')

        transcript.status = 'converted'
        transcript.save()
        logger.info('Conversion successful')
        return transcript

    except Exception as e:
        transcript.status = 'conversion-failed'
        transcript.save()
        logger.warn('Conversion failed')
        #raise
