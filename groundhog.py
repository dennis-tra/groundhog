import os
import time
import datetime
import logging
from telegram import Bot, ReplyKeyboardMarkup, Update
from telegram.ext import Updater, Job, MessageHandler, Filters
from dotenv import load_dotenv

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger()
logger.setLevel(logging.INFO)

from database import Database, GoogleSheet

answers = [
    ["5: pumped, energized", "4: happy, excited"],
    ["3: good, alright", "2: down, worried"],
    ["1: Sad, unhappy", "0: Miserable, nervous"]
]


class TelegramHandler:
    database: Database

    def __init__(self):
        self.database = GoogleSheet.from_env()

        updater = Updater(self.api_token)

        dp = updater.dispatcher
        jq = updater.job_queue

        dp.add_handler(MessageHandler(Filters.text, self.handle_reply))

        jq.run_daily(self.ask_question("🌆 How are you feeling this morning?"), datetime.time(8))
        jq.run_daily(self.ask_question("☀️ How are you feeling today?"), datetime.time(13))
        jq.run_daily(self.ask_question("🌃 How happy were you with today?"), datetime.time(22))

        jq.start()

        updater.start_polling()
        updater.idle()

    def ask_question(self, message: str):
        def send_question(bot: Bot, job: Job):
            logger.info("asking mood question")
            keyboard = ReplyKeyboardMarkup(answers)
            bot.send_message(self.chat_id, message, reply_markup=keyboard)

        return send_question

    def handle_reply(self, bot: Bot, update: Update):
        msg = update.message.text
        try:
            logger.info(f"parsing message: '{msg}'")

            is_old = update.message.date < datetime.datetime.now() - datetime.timedelta(minutes=30)
            value, answer = msg.split(":")

            if not is_old:
                message = f"Thanks I'll note that you're feeling {answer.strip().lower()}."
                bot.send_message(self.chat_id, message)

            self.database.save_mood(datetime.datetime.now(), value)

        except ValueError:
            logger.warning(f"message was not parsable: '{msg}'")
            bot.send_message(self.chat_id, "Sorry, but I did not understand your input 😕")

        except Exception as e:
            logger.error("An unknown error occurred: ", e)

    @property
    def chat_id(self) -> str:
        return os.getenv("TELEGRAM_CHAT_ID")

    @property
    def api_token(self) -> str:
        return os.getenv("TELEGRAM_API_TOKEN")


def main():
    os.environ['TZ'] = 'Europe/Berlin'
    time.tzset()

    load_dotenv()
    TelegramHandler()


if __name__ == "__main__":
    main()
