""" Main file """

import requests
from app.notion import Notion
from app.sheets import Sheets, Sheet


def is_internet():
    """ Return true if there's an internet connection,
        false otherwise """
    try:
        _ = requests.get("http://www.google.com/", timeout=2)
        return True
    except requests.ConnectionError:
        print("Internet connection error")
    return False


def main():
    """ Main part of the app which gets the data
    and creates the Sheet """
    notion = Notion()
    sheets = Sheets()

    sheet = Sheet("SheetOne", notion.memorization_times).get
    sheets.create_spreadsheet("Card Memorization", sheet)


if __name__ == "__main__":
    print("Starting app...")

    if is_internet():
        main()
