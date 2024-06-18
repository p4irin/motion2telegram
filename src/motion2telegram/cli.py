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
        phones = os.getenv('BLUETOOTH_ADDRESSES_PHONES')
        print(f'--> {phones}')
        phones = phones.split(' ')
        while True:
            for phone in phones:
                detection_status = requests.get('http://localhost:1313/0/detection/status').text.strip()

                command = [
                    'l2ping', '-c', '1', '-t', '30', phone
                ]
                try:
                    subprocess.run(['sudo'] + command, check=True)
                    # print(f'detection_status: {detection_status}')
                    if 'ACTIVE' in detection_status:
                        # print('SHOULD TURN OFF')
                        r = requests.get('http://localhost:1313/0/action/quit')
                except:
                    if 'NOT RUNNING' in detection_status:
                        # print('SHOULD TURN ON')
                        r = requests.get('http://localhost:1313/0/action/restart')
            sleep(300) 

