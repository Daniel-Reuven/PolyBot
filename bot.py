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
        num_results = 2
        video_to_search_name = incoming_msg.message.text
        temp_file = search_download_youtube_video(video_to_search_name, num_results)
        # print used parameters
        self.send_text(incoming_msg, f'Your searched for the following string: {video_to_search_name}')
        sleep(1)
        self.send_text(incoming_msg, f'Number of results set to: {num_results}')
        sleep(1)
        self.send_text(incoming_msg, 'Please wait...')
        sleep(1)
        if isinstance(temp_file, str):
            self.send_text(incoming_msg, temp_file)
        else:
            if isinstance(temp_file, list):
                for file in temp_file:
                    self.send_video(incoming_msg, context, file)


if __name__ == '__main__':
    with open('file.telegramToken') as f:
        _token = f.read()

    # Original Bot
    # my_bot = Bot(_token)
    # my_bot.start()

    # Starting a Quote Bot:
    # qbot = QuoteBot(_token)
    # qbot.start()

    # Starting a Youtube Bot:
    ytbot = YoutubeBot(_token)
    ytbot.start()
