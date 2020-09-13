import os
import time
import datetime

TIME_BETWEEN = 50  # Seconds

nightClose = False

while True:
    currDatetime = datetime.datetime.now()
    now = currDatetime.timetuple()
    dateString = f'{now[0]}-{now[1]}-{now[2]}-{now[3]}:{now[4]:02}:{now[5]:02}'
    print(f'Current Time: {dateString}')
    if now[3] < 2 or now[3] >= 17:
        TIME_BETWEEN = 50
        nightClose = False
        try:
            os.system('rm ~/RedDoorLine/images/line/*')
            os.system(f'raspistill -o ~/RedDoorLine/images/current.png'
                      f'-rot 90 -ex snow -h 808 -roi .5,.2,.333,1 -br 55')
            os.system('aws s3 cp ~/RedDoorLine/images/current.png s3://www.reddoorline.com/images/current.png')
        except Exception as e:
            print(f'Error: {e}')
            exit(1)
    else if not nightClose:
        os.system('aws s3 cp s3://www.reddoorline.com/images/status/closed.png s3://www.reddoorline.com/images/current.png')
        TIME_BETWEEN = 600
    print(f'Pausing for {TIME_BETWEEN} seconds')
    time.sleep(TIME_BETWEEN)