from django_cron import CronJobBase, Schedule


class ParseJob(CronJobBase):
    RUN_EVERY_MINS = 1

    schedule = Schedule(run_every_mins=1)
    code = 'sasta.parse_job'  # a unique code

    def do(self):
        pass
