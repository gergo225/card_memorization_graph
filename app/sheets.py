""" Sheets class file """
import pickle
import os.path
import enum
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

from app.memorization_time import MemorizationTime

# full access scope
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]


class Sheets:
    """ Class to handle Google Sheets communication

    Methods
    -------
    create_spreadsheet(title, body=Null)
        Creates a new spreadsheet with the given title
        and a starting sheet(optional) and returns it's id
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
        self.__first_sheet_id = ""

    def create_spreadsheet(self, title: str, sheet) -> str:
        """ Create a new spreadsheet with the 'title'
        and body and returns it's id

        Params
        ------
        title : str
            The title of the spreadsheet to create
        sheet : Sheet
            A JSON containing a single Sheet based on which to
            create the Spreadsheet's first sheet

        Returns
        -------
        string
            Id of the created spreadsheet
        """
        spreadsheet = {"properties": {"title": title}}
        if sheet is not None:
            spreadsheet.update({"sheets": [sheet]})
            print("Custom sheet added")

        spreadsheet = (
            self.__service.spreadsheets()  # pylint: disable=maybe-no-member
            .create(body=spreadsheet, fields="spreadsheetId,sheets")
            .execute()
        )

        print("Spreadsheet created")
        self.__first_sheet_id = spreadsheet["sheets"][0]["properties"]["sheetId"]

        return spreadsheet.get("spreadsheetId")

    def create_chart(
        self, title: str, spreadsheet_id: str, sheet_id: int, value_count: int
    ):
        """ Create a chart

        Call only after a spreadsheet with datas was created

        Parameters
        ----------
        title : str
            The title of the Chart
        spreadsheet_id : str
            The id of the spreadsheet in which to create the chart
        sheet_id : int
            The id of the sheet in the spreadsheet in which to create
            the chart
        value_count : int
            How many values must be represented on the chart
        """
        chart_request = Chart(
            title=title, sheet_id=sheet_id, value_count=value_count
        ).get_request
        request = self.__service.spreadsheets().batchUpdate( # pylint: disable=maybe-no-member
            spreadsheetId=spreadsheet_id, body=chart_request
        )
        request.execute()
        print("Chart created")

    @property
    def first_sheet_id(self):
        """ Returns the id of the first sheet (read-only)

        Accessible only after a spreadsheet was created"""
        if self.__first_sheet_id:
            return self.__first_sheet_id
        raise RuntimeError("First the create_spreadsheet must be called")


class Sheet:
    """ A Sheet in a spreadsheet """

    def __init__(self, title: str, memorization_times: list):
        """ Create a Sheet of type grid with 'title'

        Parameters
        ----------
        title: str
            The title of the sheet to create
        memorization_times: list of MemorizationTime
            A list of memorization times to include as rows in the sheet
        """
        sheet_properties = {"title": title, "index": 0}

        row_datas = [
            {
                "values": [
                    {"userEnteredValue": {"stringValue": "Date"}},
                    {"userEnteredValue": {"stringValue": "Time"}},
                ]
            }
        ]
        for memorization_time in memorization_times:
            row_data = MemorizationTimeRow(memorization_time).get
            row_datas.append(row_data)

        grid_data = {
            "startRow": 0,
            "startColumn": 0,
            "rowData": row_datas,
        }

        self.__sheet = {
            "properties": sheet_properties,
            "data": [grid_data],
        }

    @property
    def get(self):
        """ Returns the JSON representation of the created sheet (read-only) """
        return self.__sheet


class CellType(enum.Enum):
    """ The type of the cell with proper formatting """

    DATE = "DATE"
    DURATION = "TIME"


class CellData:
    """ Data about a cell in a spreadsheet """

    def __init__(self, value: str, cell_type: CellType):
        """ Create a cell with 'value' as its data

        The cell type can be of type 'DATE' or 'DURATION'
        and its format will be created accordingly
        """
        cell_format = {
            "numberFormat": CellData.get_number_format(cell_type),
        }

        self.__cell_data = {
            "userEnteredValue": {"numberValue": value},
            "userEnteredFormat": cell_format,
        }

    @property
    def get(self):
        """ Returns the JSON representation of the created cell (read-only) """
        return self.__cell_data

    @staticmethod
    def get_number_format(cell_type: str):
        """ Return the proper formatting based on the type of the cell

        Parameters
        ----------
        cell_type: CellType.DATE or CellType.DURATION
            The type of the cell

        Returns
        -------
        json
            Appropriate format based on the type of the cell

        Raises
        ------
        TypeError
            If the cell_type parameter is invalid
        """
        if cell_type == CellType.DATE:
            return {
                "type": "DATE",
                "pattern": "dd/mm/yyyy",
            }
        if cell_type == cell_type.DURATION:
            return {
                "type": "TIME",
                "pattern": '[m]":"ss',
            }
        raise TypeError()


class MemorizationTimeRow:
    """ A row created from a MemorizationTime instance """

    def __init__(self, memorization_time: MemorizationTime):
        """ Create a Row based on a MemorizationTime object

        Parameters
        ----------
        memorization_time: MemorizationTime
            The object based on which to create the row
        """
        date_cell = CellData(
            value=memorization_time.serial_date, cell_type=CellType.DATE
        ).get

        duration_cell = CellData(
            value=memorization_time.serial_duration, cell_type=CellType.DURATION
        ).get
        self.__row = {"values": [date_cell, duration_cell]}

    @property
    def get(self):
        """ Returns the JSON representation of the row (read-only) """
        return self.__row


class Chart:
    """ A Chart for representing the memorization times """

    def __init__(self, title: str, sheet_id: str, value_count: int):
        """ Create a Chart,  with the given title, from the memorization data
        on the sheet with the given sheet_id

        Parameters
        ----------
        title : str
            The title of the Chart
        sheet_id : int
            The id of the sheet in the spreadsheet in which to create
            the chart
        value_count : int
            How many values must be represented on the chart
        """
        requests = [
            {
                "addChart": {
                    "chart": {
                        "spec": {
                            "title": title,
                            "basicChart": {
                                "chartType": "LINE",
                                "legendPosition": "NO_LEGEND",
                                "axis": [
                                    {"position": "BOTTOM_AXIS", "title": "Date"},
                                    {"position": "LEFT_AXIS", "title": "Time"},
                                ],
                                "domains": [
                                    {
                                        "domain": {
                                            "sourceRange": {
                                                "sources": [
                                                    {
                                                        "sheetId": sheet_id,
                                                        "startRowIndex": 0,
                                                        "endRowIndex": value_count,
                                                        "startColumnIndex": 0,
                                                        "endColumnIndex": 1,
                                                    }
                                                ]
                                            }
                                        }
                                    }
                                ],
                                "series": [
                                    {
                                        "series": {
                                            "sourceRange": {
                                                "sources": [
                                                    {
                                                        "sheetId": sheet_id,
                                                        "startRowIndex": 0,
                                                        "endRowIndex": value_count,
                                                        "startColumnIndex": 1,
                                                        "endColumnIndex": 2,
                                                    }
                                                ]
                                            }
                                        },
                                        "targetAxis": "LEFT_AXIS",
                                    }
                                ],
                            },
                        },
                        "position": {
                            "overlayPosition": {
                                "anchorCell": {
                                    "sheetId": sheet_id,
                                    "rowIndex": 3,
                                    "columnIndex": 3,
                                },
                                "offsetXPixels": 0,
                                "offsetYPixels": 0,
                                "widthPixels": 850,
                            }
                        },
                    }
                }
            }
        ]
        self.__body = {"requests": requests}

    @property
    def get_request(self):
        """ Return JSON representation of a request to be made
        to create the specified chart (read-only) """
        return self.__body
