import os
import datetime
import json
import gspread
from telegram import Bot, ReplyKeyboardMarkup, Update
from telegram.ext import Updater, Job, MessageHandler, Filters
from oauth2client.service_account import ServiceAccountCredentials
from dotenv import load_dotenv

load_dotenv()

chat_id = os.getenv("TELEGRAM_CHAT_ID")
api_token = os.getenv("TELEGRAM_API_TOKEN")
spreadsheet_key = os.getenv("SPREADSHEET_KEY")
service_account_cred_json = json.loads(os.getenv("SERVICE_ACCOUNT_CREDENTIALS"))

scope = ['https://spreadsheets.google.com/feeds']
credentials = ServiceAccountCredentials.from_json_keyfile_dict(service_account_cred_json, scope)
gc = gspread.authorize(credentials)

book = gc.open_by_key(spreadsheet_key)
worksheet = book.worksheet("Mood")


def ask_question(message: str):
    answers = [
        ["5: pumped, energized", "4: happy, excited"],
        ["3: good, alright", "2: down, worried"],
        ["1: Sad, unhappy", "0: Miserable, nervous"]
    ]

    def send_question(bot: Bot, job: Job):
        keyboard = ReplyKeyboardMarkup(answers)
        bot.send_message(chat_id, message, reply_markup=keyboard)

    return send_question


def handle_reply(bot: Bot, update: Update):
    value, answer = update.message.text.split(":")
    message = f"Thanks I'll note that you felt {answer.strip().lower()}."
    bot.send_message(chat_id, message)
    worksheet.append_row([datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), value, answer],
                         value_input_option="USER_ENTERED")


def main():

    updater = Updater(api_token)

    dp = updater.dispatcher
    jq = updater.job_queue

    dp.add_handler(MessageHandler(Filters.text, handle_reply))

    jq.run_daily(ask_question("🌆 How are you feeling this morning?"), datetime.time(8))
    jq.run_daily(ask_question("🏙 How are you feeling today?"), datetime.time(13))
    jq.run_daily(ask_question("🌃 How happy were you with today?"), datetime.time(22))

    jq.start()

    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
