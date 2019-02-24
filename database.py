import os
import json
import datetime
import gspread
from gspread import Worksheet
from abc import ABC, abstractmethod
from oauth2client.service_account import ServiceAccountCredentials


class Database(ABC):
    @staticmethod
    @abstractmethod
    def from_env():
        pass

    @abstractmethod
    def save_mood(self, mood: int, date: datetime.date = datetime.datetime.now()):
        pass

    @abstractmethod
    def save_note(self, note: str, date: datetime.date = datetime.datetime.now()):
        pass


class GoogleSheet(Database):
    note_worksheet: Worksheet
    mood_worksheet: Worksheet

    def __init__(self, spreadsheet_key: str, mood_worksheet_name: str, note_worksheet_name: str,
                 credentials: ServiceAccountCredentials):
        gc = gspread.authorize(credentials)
        spreadsheet = gc.open_by_key(spreadsheet_key)

        self.mood_worksheet = spreadsheet.worksheet(mood_worksheet_name)
        self.note_worksheet = spreadsheet.worksheet(note_worksheet_name)
        self.date_format = "%Y-%m-%d %H:%M:%S"

    @staticmethod
    def from_env():
        scope = ['https://spreadsheets.google.com/feeds']

        credentials = os.getenv("SERVICE_ACCOUNT_CREDENTIALS")
        service_account_cred_json = json.loads(credentials)
        service_account = ServiceAccountCredentials.from_json_keyfile_dict(service_account_cred_json, scope)

        spreadsheet_key = os.getenv("SPREADSHEET_KEY")
        mood_worksheet_name = os.getenv("MOOD_WORKSHEET_NAME")
        note_worksheet_name = os.getenv("NOTE_WORKSHEET_NAME")

        return GoogleSheet(spreadsheet_key, mood_worksheet_name, note_worksheet_name, service_account)

    def save_mood(self, mood: int, date: datetime.datetime = datetime.datetime.now()):
        row = [date.strftime(self.date_format), mood]
        self.mood_worksheet.append_row(row, value_input_option="USER_ENTERED")

    def save_note(self, note: str, date: datetime.datetime = datetime.datetime.now()):
        row = [date.strftime(self.date_format), note]
        self.note_worksheet.append_row(row, value_input_option="USER_ENTERED")
