from apscheduler.jobstores.base import JobLookupError
from apscheduler.schedulers.background import BackgroundScheduler


class Scheduler:
    def __init__(self, db):
        self.sched = BackgroundScheduler(timezone='Asia/Seoul')
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

    def scheduler(self, job, type, job_id, day_of_week='mon-sun'):
        print(f"{job_id} Scheduler Starts / TYPE : {type}")
        if type == 'interval':
            self.sched.add_job(job, type, seconds=10, id=job_id, kwargs={"db": self.db})
        elif type == 'cron':  # 매일 아침 9시에 업데이트
            self.sched.add_job(job, type, day_of_week=day_of_week, hour='0', id=job_id,
                               kwargs={"db": self.db})
