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
                    zipfile.extractall(target_dir)

            # copy all others
            else:
                try:
                    os.makedirs(target_dir)
                except OSError as e:
                    if e.errno != errno.EEXIST:
                        raise
                copyfile(file.content.path, os.path.join(target_dir, filename))
                print(os.path.join(target_dir, filename))

            # docx to txt
            for extracted_file in [f for f in os.listdir(target_dir) if f.endswith('.docx')]:
                docx_to_txt(os.path.join(target_dir, extracted_file))

            # create Transcript objects
            for extracted_file in os.listdir(target_dir):
                name, extension = os.path.splitext(extracted_file)
                with open(os.path.join(target_dir, extracted_file), 'rb') as file_content:
                    transcript = Transcript(
                        name=name,
                        status='created',
                        corpus=file.corpus
                    )
                    transcript.save()
                    transcript.content.save(extracted_file, File(file_content))

            file.status = 'extracted'
            file.save()

        except:
            file.status = 'extraction-failed'
            file.save()
            raise
