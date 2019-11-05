import os, errno
from shutil import copyfile
from django_cron import CronJobBase, Schedule
from zipfile import ZipFile
from ..models import File


class ExtractJob(CronJobBase):
    RUN_EVERY_MINS = 1

    schedule = Schedule(run_every_mins=1)
    code = 'sasta.extract_job'  # a unique code

    def do(self):
        for file in File.objects.filter(status="pending"):
            print(file.content.name)
            try:
                self.extract(file)
            except Exception as error:
                print(error)

    def extract(self, file):
        file.status = 'extracting'
        file.save()
        try:
            (dir, filename) = os.path.split(file.content.name)
            target_dir = dir.replace("uploads", "extracted")
            print(target_dir)
            if filename.lower().endswith(".zip"):
                with ZipFile(file.content) as zip:
                    zip.extractall(target_dir)
            else:
                # copy file
                try:
                    os.makedirs(target_dir)
                except OSError as e:
                    if e.errno != errno.EEXIST:
                        raise
                copyfile(file.content.name, os.path.join(target_dir, filename))

            file.status = 'extracted'
            file.save()
        except:
            file.status = 'extraction-failed'
            file.save()
            raise
