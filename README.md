[![motion2telegram CI](https://github.com/p4irin/motion2telegram/actions/workflows/ci.yml/badge.svg)](https://github.com/p4irin/motion2telegram/actions/workflows/ci.yml)
# motion2telegram

> Motion is a program that monitors the video signal from one or more cameras and is able to detect if a significant part of the picture has changed. I.e., it can detect motion.

Setup a Raspberry Pi with motion2telegram to

- send a picture to a Telegram user/group if motion is detected
- activate/deactivate motion detection by scanning for the prescence of your mobile phone(s) using bluetooth

Use motion2telegram to apply a pre-configured set of motion and systemd service configuration files and Python scripts to
setup your Raspberry Pi.

## Stack

- Raspberry Pi
    - 1 B+
    - 4 B
    - Zero W V1.1
- Raspberry Pi OS
    - Lite (32-bit) (Port of Debian Bookworm)
    - Lite (64-bit)
- Python 3.11.2
- Motion 4.5.1
- Logitech C270 HD WEBCAM

## Prerequisites

- A Raspberry Pi setup with a working network configuration and connected to the internet
- The Linux BlueZ Bluetooth stack
    - Installed by default in the latest Raspberry Pi OS
- [Motion](https://motion-project.github.io/motion_build.html) installed
- A [Telegram](https://telegram.org/) account
- A Telegram [bot token](https://core.telegram.org/bots/tutorial#obtain-your-bot-token)
- The bluetooth MAC address(es) of your mobile phone(s)
- Bluetooth enabled on your mobile phone(s)
- A user on Raspberry Pi OS to run the motion service. motion2telegram installation and motion service configuration is done in the context of this user. The user MUST be a member of the groups _motion_ and _video_
- A Python virtual environment

## Install with pip

Login with the user created to run the motion service. Create a directory, e.g. motion2telegram, and cd into it. From here on, you'll work in this directory. Create and activate a Python virtual environment and then

```bash
(venv) $ pip install motion2telegram
...
# Verify by version
(venv) $ motion2telegram -V
x.y.z
(venv) $
```

## Configuration

Create a `motion.env` file with the following command.

```bash
(venv) $ motion2telegram --init
```

This file is used by

- the motion service to retrieve
    - the Telegram bot token and
    - the recipient's chat id.
- the mobile phone scanner to retrieve 
    - bluetooth MAC address(es) and
    - the scan interval

Specify your Telegram chat id and bot token in the file `motion.env`

```bash
# motion.env
TELEGRAM_BOT_TOKEN=
TELEGRAM_CHAT_ID=
```

Specify the bluetooth MAC address(es) and time between scans in `motion.env`

```bash
BLUETOOTH_ADDRESSES_PHONES=
MOBILE_PHONE_SCAN_INTERVAL=300
```

Configure motion with

```bash
(venv) $ motion2telegram --configure
```

This will install preconfigured files using the environment variables set in `motion.env` and references to Python scripts to run.

- `/etc/motion/motion.conf`
- `/lib/systemd/system/motion.service.` and
- `/lib/systemd/system/mobile_phone_scan.service`

Motion is configured to write
- logs into `log/motion.log` and
- media files into `media/YYYYMMDD`

relative to the current directory. Media captured on the same date are grouped together in a `YYYYMMDD` directory.

The motion and mobile_phone_scan systemd services will reference the `motion.env` file in the current directory for the chat id, bot token, bluetooth MAC address(es) and scan interval. The command will stop, configure and bring the motion and mobile_phone_scan service back up. If you need it, motion's process-id is written to motion.pid in the directory you installed motion2telegram.

## Reference

- [Motion](https://motion-project.github.io/)
- [Telegram](https://telegram.org/)
