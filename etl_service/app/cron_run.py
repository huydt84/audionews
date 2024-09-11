from datetime import datetime
from crontab import CronTab

tab = CronTab(tabfile='crontab.tab')
for result in tab.run_scheduler():
    print(datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
