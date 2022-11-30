from apscheduler.schedulers.background import BackgroundScheduler
from subscriptions.views import renew_subscriptions
from apscheduler.triggers.cron import CronTrigger

def start():
    scheduler = BackgroundScheduler()

    # daily at 00:00
    trigger = CronTrigger(
        month="*", day="*", day_of_week="*",  hour="0", minute="0"
    )

    scheduler.add_job(renew_subscriptions, trigger=trigger, id="subscriptionrenew_001", replace_existing=True)
    scheduler.start()