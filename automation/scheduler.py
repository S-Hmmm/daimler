from datetime import datetime as dt

from apscheduler.events import EVENT_JOB_EXECUTED, EVENT_JOB_ERROR
# from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
from apscheduler.jobstores.mongodb import MongoDBJobStore, MongoClient
from apscheduler.jobstores.memory import MemoryJobStore
# from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore


def time_work():
    print(dt.now())
    print('定时任务')


def listener(event):
    if event.exception:
        print('break')
    else:
        print(
            "job执行job:\ncode => {}\njob.id => {}\njobstore=>{}".format(
                event.code,
                event.job_id,
                event.jobstore
            ))


job_stores = {
    'mongo': MongoDBJobStore(database='apscheduler', client=MongoClient('mongodb://localhost/apscheduler')),
    'default': MemoryJobStore()
}
executors = {
    'default': ThreadPoolExecutor(20),
    'process_pool': ProcessPoolExecutor(10)
}
job_defaults = {
    'coalesce': False,
    'max_instances': 3
}


if __name__ == '__main__':
    scheduler = BlockingScheduler(jobstores=job_stores, executors=executors, job_defaults=job_defaults,
                                  timezone='Asia/Shanghai')
    scheduler.add_job(time_work, 'interval', seconds=10, id='time_work', jobstore='mongo', replace_existing=True)
    # scheduler.add_job(time_work, 'date', run_date='2021-12-17 16:57:50')
    # scheduler.add_job(time_work, 'cron', hour=10, minute='09-10', id='time_work1')
    scheduler.add_listener(listener, EVENT_JOB_EXECUTED | EVENT_JOB_ERROR)
    scheduler.pause_job(job_id='time_work')
    scheduler.print_jobs()
    scheduler.start()
    # scheduler.shutdown(wait=False)
    print('abc')
