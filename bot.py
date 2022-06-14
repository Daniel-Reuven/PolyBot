from telegram.ext import Updater, MessageHandler, Filters
from utils import search_download_youtube_video
from loguru import logger
from time import sleep


class Bot:

    def __init__(self, token):
        # create frontend object to the bot programmer
        self.updater = Updater(token, use_context=True)
        # add _message_handler as main internal msg handler
        self.updater.dispatcher.add_handler(MessageHandler(Filters.text, self._message_handler))

    def start(self):
        """Start polling msgs from users, this function never returns"""
        self.updater.start_polling()
        logger.info(f'{self.__class__.__name__} is up and listening to new messages....')
        self.updater.idle()

    def _message_handler(self, update, context):
        """Main messages handler"""
        self.send_text(update, f'Your original message: {update.message.text}')

    def send_video(self, update, context, file_path):
        """Sends video to a chat"""
        context.bot.send_video(chat_id=update.message.chat_id, video=open(file_path, 'rb'), supports_streaming=True)

    def send_text(self, update, text, quote=False):
        """Sends text to a chat"""
        # retry https://github.com/python-telegram-bot/python-telegram-bot/issues/1124
        update.message.reply_text(text, quote=quote)


class QuoteBot(Bot):
    def _message_handler(self, update, context):
        to_quote = True

        if update.message.text == 'Don\'t quote me please':
            to_quote = False

        self.send_text(update, f'Your original message: {update.message.text}', quote=to_quote)


class YoutubeBot(Bot):

    def _message_handler(self, incoming_msg, context):
        global num_results
        inbound_text = incoming_msg.message.text
        if inbound_text.startswith('?'):
            if inbound_text == '?help':
                self.send_text(incoming_msg, f'Welcome to Nicely Done Bot, This bot is simple, enter a text to search on youtube, the bot will download the video/s according to '
                                             f'defined max number of results and send you the results via this chat.')
                sleep(1)
                self.send_text(incoming_msg,
                               f'Settings mode: \n To change max number of results, type "/mnr: X" while replacing the "X" with the max number of results you would like \n Due '
                               f'to system limitations, available values are between 1-5')
                sleep(1)
                self.send_text(incoming_msg, f'Current max number of results is {num_results}')
            else:
                self.send_text(incoming_msg, 'Please use the correct command for this syntax: "?help"')
                sleep(1)
        else:
            if inbound_text.startswith('/'):
                if inbound_text.startswith('/mnr:'):
                    ivar = inbound_text[inbound_text.rindex(':') + 1:]
                    ivar.strip()
                    ivar = int(ivar)
                    self.send_text(incoming_msg, f'Settings mode detected, will attempt to update max number of results(1-5): {inbound_text}')
                    sleep(1)
                    self.send_text(incoming_msg, f'Attempting to change number of results to: {ivar}')
                    sleep(1)
                    if isinstance(ivar, int) & (1 <= ivar <= 5):
                        try:
                            num_results = ivar
                            self.send_text(incoming_msg, f'Successfully Changed to: {ivar}')
                        except:
                            self.send_text(incoming_msg, f'Unable to comply, an error has occured.')
                            print("An exception occurred")
                    else:
                        self.send_text(incoming_msg, 'Please use the correct command for this syntax, type "?help" to get more information.')
                        sleep(1)
                else:
                    self.send_text(incoming_msg, 'Please use the correct command for this syntax, type "?help" to get more information.')
                    sleep(1)
            else:
                self.send_text(incoming_msg, f'Your searched for the following string: {inbound_text}')
                sleep(1)
                self.send_text(incoming_msg, f'Number of results set to: {num_results} \n Please wait...')
                sleep(1)
                temp_file = search_download_youtube_video(inbound_text, num_results)
                if isinstance(temp_file, str):
                    self.send_text(incoming_msg, temp_file)
                else:
                    if isinstance(temp_file, list):
                        self.send_text(incoming_msg, 'Here you go: ')
                        sleep(1)
                        for file in temp_file:
                            self.send_video(incoming_msg, context, file)


if __name__ == '__main__':
    with open('.telegramToken') as f:
        _token = f.read()

    # Original Bot
    # my_bot = Bot(_token)
    # my_bot.start()

    # Starting a Quote Bot:
    # qbot = QuoteBot(_token)
    # qbot.start()

    # Starting a Youtube Bot:
    num_results = 1
    ytbot = YoutubeBot(_token)
    ytbot.start()
