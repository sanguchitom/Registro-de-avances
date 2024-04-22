import logging
from .Tasks import process_week_registers, process_task  # Importa tus tareas personalizadas
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.executors.pool import ProcessPoolExecutor, ThreadPoolExecutor
from django_apscheduler.jobstores import register_events, register_job
from django.conf import settings
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.triggers.cron import CronTrigger



# Create scheduler to run in a thread inside the application process
scheduler = BackgroundScheduler(settings.SCHEDULER_CONFIG)
scheduler = BackgroundScheduler(timezone=settings.TIME_ZONE) #Recordá poner tu zona horaria en el settings de core. en TIME_ZONE = 'UTC'
def start():
    if settings.DEBUG:
      	# Hook into the apscheduler logger
        logging.basicConfig()
        logging.getLogger('apscheduler').setLevel(logging.DEBUG)

    # Adding this job here instead of to crons.
    # This will do the following:
    # - Add a scheduled job to the job store on application initialization
    # - The job will execute a model class method at midnight each day
    # - replace_existing in combination with the unique ID prevents duplicate copies of the job
    scheduler.add_job(process_task, id="completar_dia", trigger=CronTrigger(day_of_week='*', hour=0, minute=0),replace_existing=True)
    scheduler.add_job(process_week_registers, id='register_week', trigger=CronTrigger(day_of_week='mon', hour=0, minute=30) ,replace_existing=True)
    # Add the scheduled jobs to the Django admin interfaces
    register_events(scheduler)
    scheduler.start()