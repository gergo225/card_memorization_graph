""" Sheets class file """
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# full access scope
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

# replace with valid spreadsheet id and range
SPREADHSHEET_ID = "1M4bxxPFab4YAprOV96Nofi_2S3E5iRxoUqm0AB49E9s"
SAMPLE_RANGE = "Sheet1!A1:B3"


class Sheets:
    """ Class to handle Google Sheets communication

    Methods
    -------
    """

    def __init__(self):
        creds = None
        if os.path.exists("token.pickle"):
            with open("token.pickle", "rb") as token:
                creds = pickle.load(token)

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    "credentials.json", SCOPES
                )
                creds = flow.run_local_server(port=0)

            with open("token.pickle", "wb") as token:
                pickle.dump(creds, token)

        self.__service = build("sheets", "v4", credentials=creds)

        sheet = self.__service.spreadsheets()  # pylint: disable=maybe-no-member
        result = (
            sheet.values()
            .get(spreadsheetId=SPREADHSHEET_ID, range=SAMPLE_RANGE)
            .execute()
        )
        values = result.get("values", [])

        if not values:
            print("No data found")
        else:
            for row in values:
                print(f"Name: {row[0]} \t Mark: {row[1]}")
