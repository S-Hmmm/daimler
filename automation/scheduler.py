from datetime import datetime as dt

from apscheduler.events import EVENT_JOB_EXECUTED, EVENT_JOB_ERROR
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
from apscheduler.jobstores.mongodb import MongoDBJobStore
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore


def time_work():
    print(dt.now())
    print('定时任务')


def listener(event):
    if event.exception:
        print('break')
    else:
        print('work')


job_stores = {
    'mongo': MongoDBJobStore(),
    'default': SQLAlchemyJobStore(url='sqlite:///jobs.sqlite')
}
executors = {
    'default': ThreadPoolExecutor(20),
    'process_pool': ProcessPoolExecutor(3)
}
job_defaults = {
    'coalesce': False,
    'max_instances': 3
}

scheduler = BackgroundScheduler(jobstores=job_stores, executors=executors, job_defaults=job_defaults,
                                timezone='Asia/Shanghai')
# scheduler.add_job(time_work, 'interval', seconds=3, id='time_work')
# scheduler.add_job(time_work, 'date', run_date='2021-12-17 16:57:50')
scheduler.add_job(time_work, 'cron', hour=17, minute='27-28', id='time_work')
scheduler.add_listener(listener, EVENT_JOB_EXECUTED | EVENT_JOB_ERROR)
scheduler.print_jobs()
scheduler.start()
# scheduler.shutdown(wait=False)
print('abc')
