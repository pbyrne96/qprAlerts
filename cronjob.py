from apscheduler.schedulers.background import BlockingScheduler
from send_alerts import send_alert

scheduler = BlockingScheduler()
scheduler.add_job(send_alert('home_fixtures.json').__main__(), "interval", seconds=(86400//2))