from apscheduler.schedulers.background import BlockingScheduler
from send_alerts import send_alert

scheduler = BlockingScheduler()
cls = send_alert('home_fixtures.json')
scheduler.add_job(cls.__main__, "cron", day_of_week="mon-sun",hour="09")
scheduler.start()