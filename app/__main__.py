""" Main file """

import requests
from app.notion import Notion
from app.sheets import Sheets


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
    for time in notion.memorization_times:
        print(f"Time: {time.duration} \t Date: {time.date}")


if __name__ == "__main__":
    print("Starting app...")

    # if is_internet():
    #     main()
    sheets = Sheets()
