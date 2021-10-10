import os
import time
import datetime

currDatetime = datetime.datetime.now()
now = currDatetime.timetuple()
dateString = f'{now[0]}-{now[1]}-{now[2]}-{now[3]}:{now[4]:02}:{now[5]:02}'
print(f'Current Time: {dateString}')

try:
    os.system('raspistill -o ~/RedDoorLine/images/current.png -rot 90 -ex snow -h 808 -roi .5,.2,.333,1 -br 55')
    os.system(f'cp ~/RedDoorLine/images/current.png ~/RedDoorPics/test/{dateString}.png')
    os.system('aws s3 cp ~/RedDoorLine/images/current.png s3://www.reddoorline.com/images/current.png')
except Exception as e:
    print(f'Error: {e}')
    exit(1)

