"""
The core scheduler
"""
from apscheduler.schedulers.background import BlockingScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
from pytz import timezone
from domus.utils.logger import master_log
log = master_log.name("DOMUS " + __name__)
from domus.db.jobs import JOB_STORAGE
from domus.db.influx import DataServer
from domus.twitter.tweety import Tweety
from domus.jobs.forecast import Forecast
from domus.jobs.wunderground import Wunderground
from domus.jobs.openweathermap import Openweathermap
data_storage = DataServer()
twitter_client = Tweety()

wunder = Wunderground(data_storage)
openweather = Openweathermap(data_storage)
forecast = Forecast(data_storage, twitter_client)

cache_data = wunder.run
do_forecast = forecast.run
get_coverage = openweather.run

if __name__ == '__main__':
    cba = timezone('America/Argentina/Cordoba')

    log.info("Starting Domus core...")

    jobstores = {
        'mysql': SQLAlchemyJobStore(url=JOB_STORAGE)
    }
    executors = {
        'default': ThreadPoolExecutor(20),
    }
    job_defaults = {
        'coalesce': False,
        'max_instances': 5
    }
    log.info("Starting core...")
    log.debug("Connecting to job store...")
    scheduler = BlockingScheduler(jobstores=jobstores, executors=executors, job_defaults=job_defaults, timezone=cba)
    log.debug("Creating Jobs...")
    scheduler.add_job(cache_data, 'interval', minutes=20, id='data_from_wunderground')
    scheduler.add_job(get_coverage, 'interval', minutes=5, id='data_from_openwrt')
    scheduler.add_job(do_forecast,  trigger='cron', minute='30', hour='8,13', id='twitting forecast')
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        print "quitting"
        scheduler.shutdown(wait=False)
        pass
