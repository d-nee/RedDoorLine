import os
import time
import datetime

# All time in seconds
TIME_BETWEEN_PICTURES = 50
TIME_BETWEEN_CLOSED_CHECK = 600

# 24HR Time
HOUR_CLOSE = 2
HOUR_OPEN = 17

nightClose = False

TIME_BETWEEN = TIME_BETWEEN_PICTURES

while True:
    currDatetime = datetime.datetime.now()
    now = currDatetime.timetuple()
    dateString = f'{now[0]}-{now[1]}-{now[2]}-{now[3]}:{now[4]:02}:{now[5]:02}'
    print(f'Current Time: {dateString}')
    if now[3] < HOUR_CLOSE or now[3] >= HOUR_OPEN:
        TIME_BETWEEN = TIME_BETWEEN_PICTURES
        nightClose = False
        try:
            os.system('rm ~/RedDoorLine/images/line/*')
            os.system(f'raspistill -o ~/RedDoorLine/images/current.png' + \
                      f' -rot 90 -ex snow -h 808 -roi .5,.2,.333,1 -br 55')
            os.system('aws s3 cp ~/RedDoorLine/images/current.png s3://www.reddoorline.com/images/current.png')
        except Exception as e:
            print(f'Error: {e}')
            exit(1)
    elif not nightClose:
        os.system('aws s3 cp s3://www.reddoorline.com/images/status/closed.png s3://www.reddoorline.com/images/current.png')
        TIME_BETWEEN = TIME_BETWEEN_CLOSED_CHECK
        nightClose = True
    print(f'Pausing for {TIME_BETWEEN} seconds')
    time.sleep(TIME_BETWEEN)