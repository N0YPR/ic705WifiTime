import subprocess
import shlex
import sys
from time import sleep

from icom import IC705
from sys import platform

if __name__ == '__main__':
    if not (platform == "linux" or platform == "linux2"):
        print('OS not supported')
        exit(1)

    args = sys.argv[1:]
    port = args[0]

    icom = IC705(port=port)

    print('Turning off NTP sync...', end='')
    sys.stdout.flush()
    subprocess.call(shlex.split('sudo timedatectl set-ntp off'))
    print("done.")

    print("Waiting up to 60 seconds for accurate time...", end='')
    sys.stdout.flush()

    time = icom.read_time_setting()
    while True:
        new_time = icom.read_time_setting()
        if new_time != time:
            time = new_time
            break
        sleep(0.01)

    date = icom.read_date_setting()

    datetime_string = f'{date[0]:04}-{date[1]:02}-{date[2]:02} {time[0]:02}:{time[1]:02}:00 UTC'
    print(datetime_string)

    print(f'Setting system and hardware time to {datetime_string}', end='')
    sys.stdout.flush()
    subprocess.call(shlex.split(f"sudo timedatectl set-time '{datetime_string}'"))
    subprocess.call(shlex.split('sudo hwclock -w'))
    print("done.")

    print('Turning NTP sync back on.', end='')
    sys.stdout.flush()
    subprocess.call(shlex.split('sudo timedatectl set-ntp on'))
    print("done.")


