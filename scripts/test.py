import os
import time
import datetime

IMG_PATH = '~/RedDoorLine/images/current.png'

currDatetime = datetime.datetime.now()
now = currDatetime.timetuple()
dateString = f'{now[0]}-{now[1]}-{now[2]}-{now[3]}:{now[4]:02}:{now[5]:02}'
print(f'Current Time: {dateString}')

try:
        os.system(f'raspistill -o {IMG_PATH} -vf -hf -ex snow -roi .3,.5,.7,.25')
        os.system(f'convert -pointsize 100 -fill yellow -draw "text 0,100 \'$(date)\'" {IMG_PATH} {IMG_PATH}')
        os.system(f'cp {IMG_PATH} ~/RedDoorPics/test/{dateString}.png')
        os.system(f'aws s3 cp {IMG_PATH} s3://www.reddoorline.com/images/current.png')
except Exception as e:
    print(f'Error: {e}')
    exit(1)

