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
    def save_mood(self, date: datetime.date, mood: int):
        pass


class GoogleSheet(Database):
    worksheet: Worksheet

    def __init__(self, spreadsheet_key: str, worksheet_name: str, credentials: ServiceAccountCredentials):
        gc = gspread.authorize(credentials)
        spreadsheet = gc.open_by_key(spreadsheet_key)

        self.worksheet = spreadsheet.worksheet(worksheet_name)
        self.date_format = "%Y-%m-%d %H:%M:%S"

    @staticmethod
    def from_env():
        scope = ['https://spreadsheets.google.com/feeds']

        credentials = os.getenv("SERVICE_ACCOUNT_CREDENTIALS")
        service_account_cred_json = json.loads(credentials)
        service_account = ServiceAccountCredentials.from_json_keyfile_dict(service_account_cred_json, scope)

        spreadsheet_key = os.getenv("SPREADSHEET_KEY")
        worksheet_name = os.getenv("WORKSHEET_NAME")

        return GoogleSheet(spreadsheet_key, worksheet_name, service_account)

    def save_mood(self, date: datetime.datetime, mood: int):
        row = [date.strftime(self.date_format), mood]
        self.worksheet.append_row(row, value_input_option="USER_ENTERED")
