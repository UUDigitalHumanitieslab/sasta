import errno
import os
from shutil import copyfile
from zipfile import ZipFile

from django.core.files import File
from django_cron import CronJobBase, Schedule

from ..models import Transcript, UploadFile
from ..utils import docx_to_txt


class ExtractJob(CronJobBase):
    RUN_EVERY_MINS = 1

    schedule = Schedule(run_every_mins=1)
    code = 'sasta.extract_job'  # a unique code

    def do(self):
        for file in UploadFile.objects.filter(status="pending"):
            try:
                self.extract(file)
            except Exception as error:
                print(error)

    def extract(self, file):
        file.status = 'extracting'
        file.save()

        try:
            (origin_dir, filename) = os.path.split(file.content.path)
            target_dir = origin_dir.replace('uploads', 'extracted')
            # extract zipped files
            if filename.lower().endswith(".zip"):
                with ZipFile(file.content) as zipfile:
                    for zip_name in zipfile.namelist():
                        zipfile.extract(zip_name, path=target_dir)
                        extracted_path = os.path.join(target_dir, zip_name)
                        self.create_transcript(file, extracted_path)
            # copy all others
            else:
                try:
                    os.makedirs(target_dir)
                except OSError as e:
                    if e.errno != errno.EEXIST:
                        raise
                new_path = os.path.join(target_dir, filename)
                copyfile(file.content.path, os.path.join(target_dir, filename))
                self.create_transcript(file, new_path)

            file.status = 'extracted'
            file.save()

        except:
            file.status = 'extraction-failed'
            file.save()
            raise

    def create_transcript(self, file, content_path):
        if content_path.endswith('.docx'):
            docx_to_txt(content_path)
            content_path = content_path.replace('.docx', '.txt')

        _dir, filename = os.path.split(content_path)

        with open(content_path, 'rb') as file_content:
            transcript = Transcript(
                name=filename.strip('.txt'),
                status='created',
                corpus=file.corpus
            )
            transcript.save()
            transcript.content.save(filename, File(file_content))
