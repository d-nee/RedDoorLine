import os
import time
import datetime

TIME_BETWEEN = 50  # Seconds

openTime_dict = {0 : 7, 1 : 7, 2: 7, 3 : 7, 4 : 7, 5 : 15, 6 : 15}
nightClose = False

while True:
    currDatetime = datetime.datetime.now()
    now = currDatetime.timetuple()
    dateString = f'{now[0]}-{now[1]}-{now[2]}-{now[3]}:{now[4]:02}:{now[5]:02}'
    print(f'Current Time: {dateString}')
    # openTime = openTime_dict[now[6]]
    if now[3] < 2 or now[3] >= 17:
        TIME_BETWEEN = 50
        nightClose = False
        try:
            imgName = f"rdLine@{dateString}.jpg"
            os.system('rm ~/RedDoorLine/images/line/*')
            os.system(f'raspistill -o ~/RedDoorLine/images/line/{imgName} '
                      f'-rot 90 -ex snow -h 808 -roi .5,.2,.333,1 -br 55')
            # os.system(f'cp ~/RedDoorLine/images/{imgName} ~/RedDoorPics')
        except Exception as e:
            print(f'Error: {e}')
            exit(1)
    else:
        TIME_BETWEEN = 600
    print(f'Pausing for {TIME_BETWEEN} seconds')
    time.sleep(TIME_BETWEEN)