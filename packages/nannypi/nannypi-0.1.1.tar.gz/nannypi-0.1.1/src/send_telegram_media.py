#! /usr/bin/env python

"""
    Script will send telegram files via cli options.
    This will pull Telegram token and 
"""

import argparse
import os
import telegram


class TelegramSender:
    """
        Telegram sender simplifies the telegram bot code down to simply sending files.
    """

    def send_file(self, filename, caption=None):
        """ Send file with optional caption."""

        # crash if file does not exist.
        if not os.path.exists(filename):
            raise FileNotFoundError(f"The file {filename} does not exist.")

        # extract the lowercase filename.
        extension = os.path.splitext(filename)[1].lower()

        # send an image.
        if extension in ['.jpg', '.png', '.gif']:
            self.bot.send_photo(chat_id=self.chat_id, photo=open(filename, 'rb'), caption=caption)

        # send a video
        elif extension in ['.avi', '.mpg']:
            self.bot.send_video(chat_id=self.chat_id, video=open(filename, 'rb'), caption=caption)

        # send any other type of file.
        else:
            self.bot.send_document(chat_id=chat_id, document=open(filename, 'rb'), caption=caption)

    def get_me(self):
        """ print bot id info """
        print(self.bot.get_me())

    def __init__(self, token, chat_id):
        """ init with chat id and token """

        self.token = token
        self.bot = telegram.Bot(token=self.token)
        self.chat_id = chat_id


if __name__ == '__main__':

    # cli arguments
    parser = argparse.ArgumentParser(description="Send media images to a Telegram Chat.")
    parser.add_argument("-f", "--file", nargs='*',
        help="Files to send")
    parser.add_argument("-t", "--token", default=None,
        help="telegram token. Can also be specified with the env variable TELEGRAM_BOT_TOKEN.")
    parser.add_argument("-c", "--chat-id", dest='chat_id', default=None,
        help="telegram chat id.  Can also be specified with the env variable TELEGRAM_CHAT_ID")
    args = parser.parse_args()

    # set token - precidence goes to the cli argument
    if args.token:
        telegram_token = args.token
    else:
        telegram_token = os.getenv("TELEGRAM_BOT_TOKEN")
    
    # set chat_id = precidence goes to the cli argument
    if args.chat_id:
        telegram_chat_id = args.chat_id
    else:
        telegram_chat_id = os.getenv("TELEGRAM_CHAT_ID")

    # initialize sender.
    sender = TelegramSender(telegram_token, telegram_chat_id)

    # send files
    for this_file in args.file:
        sender.send_file(this_file, caption=this_file)
