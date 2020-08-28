""" Sheets class file """
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# full access scope
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]


class Sheets:
    """ Class to handle Google Sheets communication

    Methods
    -------
    create_spreadsheet(title)
        Creates a new spreadsheet with the given title
        and returns it's id
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

    def create_spreadsheet(self, title: str) -> str:
        """ Create a new spreadsheet with the 'title'
        and returns it's id

        Params
        ------
        title : str
            The title of the spreadsheet to create

        Returns
        -------
        string
            Id of the created spreadsheet
        """
        spreadsheet = {"properties": {"title": title}}
        spreadsheet = (
            self.__service.spreadsheets()  # pylint: disable=maybe-no-member
            .create(body=spreadsheet, fields="spreadsheetId")
            .execute()
        )

        return spreadsheet.get("spreadsheetId")
