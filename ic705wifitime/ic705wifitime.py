import serial
import subprocess
import shlex
import sys
import time

def get_time_from_civ(port):
    ser = serial.Serial(port)
    command = b'\x1a\x05'
    time_subcommand = b'\x01\x66'
    date_subcommand = b'\x01\x65'
    
    ser.write(b'\xfe\xfe\xa4\xe0' + command + date_subcommand + b'\xfd')
    ser.read_until(expected=b'\xfd')

    date_reply = ser.read_until(expected=b'\xfd')
    
    ser.write(b'\xfe\xfe\xa4\xe0' + command + time_subcommand + b'\xfd')
    ser.read_until(expected=b'\xfd')

    time_reply = ser.read_until(expected=b'\xfd')

    time_string = f'{date_reply[8]:02x}{date_reply[9]:02x}-{date_reply[10]:02x}-{date_reply[11]:02x} {time_reply[8]:02x}:{time_reply[9]:02x}:00 UTC'
    
    return time_string

def get_new_time_from_civ(port):
    time_str = get_time_from_civ(port)
    while True:
        new_time_str = get_time_from_civ(port)
        if new_time_str != time_str:
            time_str = new_time_str
            break
        time.sleep(0.01)
    return time_str

def set_time_from_ic705(host):
    print('Turning off NTP sync...', end='')
    sys.stdout.flush()
    subprocess.call(shlex.split('sudo timedatectl set-ntp off'))
    print("done.")

    print("Waiting up to 60 seconds for accurate time...", end='')
    sys.stdout.flush()

    port = f'/tmp/kappanhang-{host}.pty'
    time_str = get_new_time_from_civ(port)
    print("done.")

    print(f'Setting system and hardware time to {time_str}', end='')
    sys.stdout.flush()
    subprocess.call(shlex.split(f"sudo timedatectl set-time '{time_str}'"))
    subprocess.call(shlex.split('sudo hwclock -w'))
    print("done.")
    
    print('Turning NTP sync back on.', end='')
    sys.stdout.flush()
    subprocess.call(shlex.split('sudo timedatectl set-ntp on'))
    print("done.")
    
if __name__ == "__main__":
    args = sys.argv[1:]
    set_time_from_ic705(args[0])

    