import os
import datetime
import logging
from telegram import Bot, ReplyKeyboardMarkup, Update
from telegram.ext import Updater, Job, MessageHandler, Filters, ConversationHandler, CommandHandler, RegexHandler
from dotenv import load_dotenv

from database import Database, GoogleSheet

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger()
logger.setLevel(logging.INFO)

answers = [
    ["5: pumped, energized", "4: happy, excited"],
    ["3: good, alright", "2: down, worried"],
    ["1: Sad, unhappy", "0: Miserable, nervous"]
]

TEXT_NOTE = range(1)


class TelegramHandler:
    database: Database

    def __init__(self):
        self.database = GoogleSheet.from_env()

        updater = Updater(self.api_token)

        dp = updater.dispatcher
        jq = updater.job_queue

        mood_handler = RegexHandler(r"\d:\D*", self.handle_mood)
        dp.add_handler(mood_handler)

        note_handler = ConversationHandler(
            entry_points=[CommandHandler("note", self.handle_note)],
            states={
                TEXT_NOTE: [MessageHandler(Filters.text, self.save_note)]
            },
            fallbacks=[CommandHandler('cancel', self.cancel_note)]
        )
        dp.add_handler(note_handler)

        stats_handler = CommandHandler("stats", self.stats)
        dp.add_handler(stats_handler)

        jq.run_daily(self.ask_question("🌆 How are you feeling this morning?"), datetime.time(8))
        jq.run_daily(self.ask_question("☀️ How are you feeling today?"), datetime.time(13))
        jq.run_daily(self.ask_question("🌃 How happy were you with today?"), datetime.time(22))

        jq.start()

        updater.start_polling()
        updater.idle()

    def stats(self, bot: Bot, update: Update):
        update.message.reply_text(f"Hang tight I'm calculating your statistics... 🧮")
        moods = self.database.get_moods()

        update.message.reply_text(f"Total tracked moods: {len(moods)}")

    def save_note(self, bot: Bot, update: Update):
        bot.send_message(self.chat_id, "Got it! I'll forever remember this note for you 📚")
        self.database.save_note(update.message.text, datetime.datetime.now())
        return ConversationHandler.END

    def handle_note(self, bot: Bot, update: Update):
        update.message.reply_text("Alright, let me know what you want to note 📝")
        return TEXT_NOTE

    def cancel_note(self, bot: Bot, update: Update):
        bot.send_message(self.chat_id, "No worries, I won't note anything.")
        return ConversationHandler.END

    def ask_question(self, message: str):
        def send_question(bot: Bot, job: Job):
            logger.info("asking mood question")
            keyboard = ReplyKeyboardMarkup(answers)
            bot.send_message(self.chat_id, message, reply_markup=keyboard)

        return send_question

    def handle_mood(self, bot: Bot, update: Update):
        msg = update.message.text
        try:
            logger.info(f"parsing message: '{msg}'")

            is_old = update.message.date < datetime.datetime.now() - datetime.timedelta(minutes=30)
            rating, answer = msg.split(":")
            rating = int(rating)

            self.database.save_mood(rating, datetime.datetime.now())

            if is_old:
                return

            message = f"Got it! I'll note that you're feeling {answer.strip().lower()}."
            update.message.reply_text(message)

            if rating <= 1:
                bad_mood_msg = "Feeling down sometimes is okay. Maybe take 2 minutes to reflect on why you're not " \
                               "feeling better, and optionally add a /note. "
                update.message.reply_text(bad_mood_msg)

            if rating == 5:
                good_mood = "💫 Awesome to hear, maybe take 2 minutes to reflect on why you're feeling great," \
                            " and optionally add a /note."
                update.message.reply_text(good_mood)

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
    load_dotenv()
    TelegramHandler()


if __name__ == "__main__":
    main()
