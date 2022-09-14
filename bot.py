# YoutubeDownloadApp Bot version 1
#   this bot is designed to receive a string from user input
#   then search a video/s on YouTube matching the string
#   then download the video/s(if not already exists in 'ytdlAppData' directory), while based on predefined limitations for guaranteeing performance
#   then send the video/s to user
#   standby for new user input
# Parameters:
#
# ?help (?help): display help menu
# /mnr: X (/mnr: X): display the settings menu, for more information, can review help menu


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
        # Define number of results based on global variable
        global num_results
        # Define user input into variable
        inbound_text = incoming_msg.message.text
        # Check if the user is trying to use the help menu
        if inbound_text.startswith('?'):
            if inbound_text == '?help':
                # Check if the user is trying to use the help menu and respond to correct input with relevant information
                self.send_text(incoming_msg, f'Welcome to Nicely Done Bot, This bot is simple, enter a text to search on youtube, the bot will download the video/s according to '
                                             f'defined max number of results and send you the results via this chat.')
                # Show information on Settings mode
                sleep(1)
                self.send_text(incoming_msg,
                               f'Settings mode: \nTo change max number of results, type "/mnr: X" while replacing the "X" with the max number of results you would like \nDue '
                               f'to system limitations, available values are between 1-5')
                self.send_text(incoming_msg, f'Current max number of results is {num_results}')
            else:
                # Respond with example syntax for help menu
                self.send_text(incoming_msg, 'Please use the correct command for this syntax: "?help"')
                sleep(1)
        else:
            # Check if the user is trying to use the Settings menu
            if inbound_text.startswith('/'):
                if inbound_text.startswith('/mnr:'):
                    # Extract selected value from user input for verification
                    ivar = inbound_text[inbound_text.rindex(':') + 1:]
                    ivar = ivar.strip()
                    allowed_values = ["1", "2", "3", "4", "5"]
                    # Verifying user input for settings mode
                    if ivar not in allowed_values:
                        self.send_text(incoming_msg, 'Please use the correct command for this syntax, type "?help" to get more information.')
                        sleep(1)
                    else:
                        # Convert to type int
                        ivar = int(ivar)
                        self.send_text(incoming_msg, f'Settings mode detected, will attempt to update max number of results(1-5): {inbound_text}')
                        sleep(1)
                        self.send_text(incoming_msg, f'Attempting to change number of results to: {ivar}')
                        sleep(1)
                        # Try to update max number of results
                        try:
                            num_results = ivar
                            self.send_text(incoming_msg, f'Successfully Changed to: {ivar}')
                        except:
                            self.send_text(incoming_msg, f'Unable to comply, an error has occurred.')
                            print("An exception occurred")
                else:
                    self.send_text(incoming_msg, 'Please use the correct command for this syntax, type "?help" to get more information.')
                    sleep(1)
            else:
                # Continue to youtube download mode
                self.send_text(incoming_msg, f'Your searched for the following: {inbound_text}')
                sleep(1)
                self.send_text(incoming_msg, f'Number of results set to: {num_results} \nPlease wait...')
                sleep(1)
                temp_file = search_download_youtube_video(inbound_text, num_results, s3_bucket_name)
                if isinstance(temp_file, str):
                    self.send_text(incoming_msg, temp_file)
                else:
                    if isinstance(temp_file, list):
                        self.send_text(incoming_msg, 'Here are your results: ')
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

    # Define initial max number of results
    num_results = 1
    s3_bucket_name = 'daniel-reuven-awsdemo-bucket'
    # Starting a YouTube Bot:
    ytbot = YoutubeBot(_token)
    ytbot.start()
