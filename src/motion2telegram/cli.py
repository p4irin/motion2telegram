import os
import requests
import subprocess
from time import sleep
import argparse
from . import __version__
from .configure import configure, init
from .send import send

def cli() -> None:
    parser = argparse.ArgumentParser(
        description='Configure the motion service or send a picture to a Telegram user/group',
        epilog=''
    )

    parser.add_argument(
        '-V', '--version',
        action='version',
        version=f'{__version__}',
        help='Show version and exit'
    )

    parser.add_argument(
        '-i', '--init',
        action='store_true',
        help='Create a motion.env file to specify your Telegram bot token and chat/group id'
    )

    parser.add_argument(
        '-c', '--configure',
        action='store_true',
        help='Configure the motion service'
    )

    parser.add_argument(
        '-p', '--picture',
        action='store',
        help='Picture to send to a Telegram user/group'
    )

    parser.add_argument(
        '-s', '--scan',
        action='store_true',
        help='Scan mobile phones'
    )


    args = parser.parse_args()

    if args.init:
        init()
        print('Created a "motion.env" file in the current directory')
        print('Specify your Telegram bot token and chat/group id in it and '
              + 'then run "motion2telegram --configure"')
        
    if args.configure:
        configure()

    if args.picture:
        send(args.picture)

    if args.scan:
        base_url = 'http://localhost:1313/0'
        phones = os.getenv('BLUETOOTH_ADDRESSES_PHONES')
        phones = phones.split(' ') # type: ignore
        scan_interval = int(os.getenv('MOBILE_PHONE_SCAN_INTERVAL')) # type: ignore
        while True:
            for phone in phones: # type: ignore
                detection_status = requests.get(
                    f'{base_url}/detection/status'
                ).text.strip()

                command = [
                    'l2ping', '-c', '1', '-t', '30', phone
                ]
                try:
                    subprocess.run(['sudo'] + command, check=True)
                    if 'ACTIVE' in detection_status:
                        requests.get(f'{base_url}/action/quit')
                except Exception:
                    if 'NOT RUNNING' in detection_status:
                        requests.get(f'{base_url}/action/restart')
            sleep(scan_interval)

