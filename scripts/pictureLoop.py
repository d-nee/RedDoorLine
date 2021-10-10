import os
import time
import datetime

IMG_PATH = '~/RedDoorLine/images/current.png'

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
            os.system(f'raspistill -o {IMG_PATH} -vf -hf -ex snow -roi .3,.5,.7,.25')
            os.system(f'convert -pointsize 100 -fill yellow -draw "text 0,100 \'$(date)\'" {IMG_PATH} {IMG_PATH}')
            os.system(f'cp {IMG_PATH} ~/RedDoorPics/{dateString}.png')
            os.system(f'aws s3 cp {IMG_PATH} s3://www.reddoorline.com/images/current.png')
        except Exception as e:
            print(f'Error: {e}')
            exit(1)
    elif not nightClose:
        os.system('aws s3 cp s3://www.reddoorline.com/images/status/closed.png s3://www.reddoorline.com/images/current.png')
        TIME_BETWEEN = TIME_BETWEEN_CLOSED_CHECK
        nightClose = True
    print(f'Pausing for {TIME_BETWEEN} seconds')
    time.sleep(TIME_BETWEEN)