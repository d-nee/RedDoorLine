import os
import time
import datetime

IMG_PATH = '~/RedDoorLine/images/current.png'
LOG_PATH = '~/RedDoorLine/log.txt'

# Pixels of Height, like 1080p, but now ___p
# Ideally divisible by 3
RES = 225

# All time in seconds
TIME_BETWEEN_PICTURES = 50
TIME_BETWEEN_CLOSED_CHECK = 600

# 24HR Time
HOUR_CLOSE = 2
HOUR_OPEN = 17

nightClose = False

TIME_BETWEEN = TIME_BETWEEN_PICTURES

def run():
    global nightClose
    currDatetime = datetime.datetime.now()
    now = currDatetime.timetuple()
    dateString = f'{now[0]}-{now[1]:02}-{now[2]:02}_{now[3]:02}-{now[4]:02}-{now[5]:02}'
    # print(f'Current Time: {dateString}')
    if now[3] < HOUR_CLOSE or now[3] >= HOUR_OPEN:
        TIME_BETWEEN = TIME_BETWEEN_PICTURES
        nightClose = False
        try:
            os.system(f'raspistill -n -o {IMG_PATH} -vf -hf -ex snow -roi .25,.5,.7,.25')
            os.system(f'convert {IMG_PATH} -resize {RES*8//3}x{RES}! {IMG_PATH}')
            os.system(f'convert -pointsize {RES//15} -fill yellow -draw "text 0,{RES//15} \'{dateString}\'" {IMG_PATH} {IMG_PATH}')
            os.system(f'cp {IMG_PATH} /media/pi/DNEE/{dateString}.png')
            os.system(f'echo {dateString} >> {LOG_PATH}')
            os.system(f'aws s3 cp {IMG_PATH} s3://www.reddoorline.com/images/current.png')
        except Exception as e:
            print(f'Error: {e}')
            exit(1)
    elif not nightClose:
        os.system('aws s3 cp s3://www.reddoorline.com/images/status/closed.png s3://www.reddoorline.com/images/current.png')
        TIME_BETWEEN = TIME_BETWEEN_CLOSED_CHECK
        nightClose = True
    # print(f'Pausing for {TIME_BETWEEN} seconds')
    time.sleep(TIME_BETWEEN)

if __name__ == '__main__':
    while True:
        run()