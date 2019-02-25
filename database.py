import os
import json
import datetime
import dateparser
import gspread
import requests
from typing import List
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

    @abstractmethod
    def get_moods(self) -> (List[datetime.datetime], List[int]):
        pass


class GoogleSheet(Database):
    credentials: ServiceAccountCredentials
    note_worksheet: Worksheet
    mood_worksheet: Worksheet

    def __init__(self, spreadsheet_key: str, mood_worksheet_name: str, note_worksheet_name: str,
                 credentials: ServiceAccountCredentials):

        self.credentials = credentials
        self.spreadsheet_key = spreadsheet_key
        self.mood_worksheet_name = mood_worksheet_name
        self.note_worksheet_name = note_worksheet_name

        self.authenticate()

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
        try:
            self.mood_worksheet.append_row(row, value_input_option="USER_ENTERED")
        except gspread.exceptions.APIError as e:
            if e.response.json()['error']['code'] == 401:
                self.authenticate()
                self.save_mood(mood, date)

    def save_note(self, note: str, date: datetime.datetime = datetime.datetime.now()):
        row = [date.strftime(self.date_format), note]
        try:
            self.note_worksheet.append_row(row, value_input_option="USER_ENTERED")
        except gspread.exceptions.APIError as e:
            if e.response.json()['error']['code'] == 401:
                self.authenticate()
                self.save_note(note, date)

    def authenticate(self):

        gc = gspread.authorize(self.credentials)
        spreadsheet = gc.open_by_key(self.spreadsheet_key)

        self.mood_worksheet = spreadsheet.worksheet(self.mood_worksheet_name)
        self.note_worksheet = spreadsheet.worksheet(self.note_worksheet_name)

    def get_moods(self) -> (List[datetime.datetime], List[int]):

        dates = list(map(lambda d: dateparser.parse(d), self.mood_worksheet.col_values(1)))
        moods = list(map(int, self.mood_worksheet.col_values(2)))

        return dates, moods

