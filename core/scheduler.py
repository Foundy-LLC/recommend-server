from apscheduler.jobstores.base import JobLookupError
from apscheduler.schedulers.background import BackgroundScheduler


class Scheduler:
    def __init__(self, job, db):
        self.sched = BackgroundScheduler(timezone='Asia/Seoul')
        self.job = job
        self.db = db
        self.sched.start()
        self.job_name = ''

    def __del__(self):
        self.shutdown()

    def shutdown(self):
        self.sched.shutdown()

    def kill_scheduler(self, job_name):
        try:
            self.sched.remove_job(job_name)
        except JobLookupError as err:
            print("fail to stop Scheduler: {err}".format(err=err))
            return

    def scheduler(self, type, job_id):
        print(f"{job_id} Scheduler Starts / TYPE : {type}")
        if type == 'interval':
            self.sched.add_job(self.job, type, seconds=10, id=job_id)
        elif type == 'cron':
            self.sched.add_job(self.job, type, day_of_week='mon-sun', hour='6', id=job_id,
                               kwargs={"db": self.db})
