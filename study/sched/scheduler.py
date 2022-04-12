from datetime import datetime as dt

from apscheduler.events import EVENT_JOB_EXECUTED, EVENT_JOB_ERROR
from apscheduler.schedulers.background import BackgroundScheduler
# from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
from apscheduler.jobstores.mongodb import MongoDBJobStore, MongoClient
from apscheduler.jobstores.memory import MemoryJobStore
from apscheduler.triggers.interval import IntervalTrigger


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
    'max_instances': 5
}

scheduler = BackgroundScheduler(jobstores=job_stores,
                                executors=executors,
                                job_defaults=job_defaults,
                                timezone='Asia/Shanghai',
                                )

if __name__ == '__main__':
    print('JOBS', scheduler.get_jobs())
    if scheduler.get_jobs(jobstore='default'):
        scheduler.remove_all_jobs(jobstore='default')

    interval_trigger = IntervalTrigger(seconds=10, timezone='Asia/Shanghai')
    scheduler.add_job(time_work, trigger=interval_trigger, id='time_work',
                      jobstore='default', replace_existing=True)
    scheduler.add_job(time_work, 'date', run_date='2022-01-13 14:01:10', id='ot')
    scheduler.add_job(time_work, 'cron', hour=13, minute='55', id='time_work',
                      jobstore='mongo', replace_existing=True)

    scheduler.add_listener(listener, EVENT_JOB_EXECUTED | EVENT_JOB_ERROR)
    # scheduler.pause_job(job_id='time_work')
    # scheduler.print_jobs()
    scheduler.start()
    # scheduler.shutdown(wait=False)
    while 1:
        if not scheduler.get_jobs(jobstore='default'):
            break
