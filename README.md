# motion2telegram

> Motion is a program that monitors the video signal from one or more cameras and is able to detect if a significant part of the picture has changed. I.e., it can detect motion.

motion2telegram applies a pre-configured set of motion and systemd service configuration files and a script to send a message including a picture to a Telegram user/group when motion is detected.

The intent of motion2telegram is to enable me to quickly setup a Raspberry Pi with a webcam to notify me through Telegram when motion is detected.

## Stack

- Raspberry Pi 1 B+
- Raspberry Pi OS Lite (32-bit) (Port of Debian Bookworm)
- Python 3.11.2
- Motion 4.5.1
- Logitech C270 HD WEBCAM

## Prerequisites

- A Raspberry Pi setup with a working network configuration and connected to the internet
- [Motion](https://motion-project.github.io/motion_build.html) installed
- A [Telegram](https://telegram.org/) account
- A Telegram [bot token](https://core.telegram.org/bots/tutorial#obtain-your-bot-token)
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

Create a motion.env file with the following command.

```bash
(venv) $ motion2telegram --init
```

This file is used by the motion service to retrieve the Telegram bot token and the recipient's chat id.

Specify your Telegram chat id and bot token in the file motion.env

```bash
# motion.env
TELEGRAM_BOT_TOKEN=
TELEGRAM_CHAT_ID=
```

Configure motion with

```bash
(venv) $ motion2telegram --configure
```

This will install /etc/motion/motion.conf and /lib/systemd/system/motion.service.

Motion is configured to write logs into log/motion.log and media files into media/YYYYMMDD relative to the current directory. Media captured on the same date are grouped together in a YYYYMMDD directory.

The motion systemd service will reference the motion.env file in the current directory for the chat id and the bot token. The command will stop, configure and bring the motion service back up.

## Reference

- [Motion](https://motion-project.github.io/)
- [Telegram](https://telegram.org/)