# nannypi

This project is to create a telegram-enabled nanny cam using a raspberry pi and a usb webcam.

## Project Installation

Run the script

Edit the /etc/default/motion file: `sudo vim /etc/default/motion`

```
# set to 'yes' to enable the motion daemon
start_motion_daemon=yes

TELEGRAM_BOT_TOKEN=<telegram_bot_token>
TELEGRAM_CHAT_ID=<telegram_chat_id>

export TELEGRAM_BOT_TOKEN
export TELEGRAM_CHAT_ID
```

Edit motion config file: `sudo vim /etc/motion/motion.conf`
The option `on_picture_save` is commented out.  Remove the comment and add the following.

```
on_picture_save /opt/nannypi/venv/bin/send_telegram_media.py --delete --file %f
```

## Python Script info

This is part of a larger repo created to create a telegram-enabled nanny camera.  See the main repo for full information: [nannypi](https://gitlab.com/rveach/nannypi).

### Install Python Scripts

```bash
pip install nannypi
```

### send_telegram_media.py

This script will send media to telegram using cli arguments.

```bash
python send_telegram_media.py -h
usage: send_telegram_media.py [-h] [-f [FILE [FILE ...]]] [-t TOKEN]
                              [-c CHAT_ID] [-d]

Send media images to a Telegram Chat.

optional arguments:
  -h, --help            show this help message and exit
  -f [FILE [FILE ...]], --file [FILE [FILE ...]]
                        Files to send
  -t TOKEN, --token TOKEN
                        telegram token. Can also be specified with the env
                        variable TELEGRAM_BOT_TOKEN.
  -c CHAT_ID, --chat-id CHAT_ID
                        telegram chat id. Can also be specified with the env
                        variable TELEGRAM_CHAT_ID
  -d, --delete          delete file after sending
```