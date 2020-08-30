""" Notion class file """

from notion.client import NotionClient
from app import my_secrets
from app.memorization_time import MemorizationTime

class Notion:
    """ Class for communicating with Notion
    and storing the memorization times

    Attribues
    ---------
    memorization_times : list of MemorizationTime
        Stores the memorization times ordered by date
    """

    def __init__(self):
        """ Initialize Notion client and other variables
        and get all memorization times

        First checks the internet connection
        """
        self.__memorization_times = []

        client = NotionClient(token_v2=my_secrets.TOKEN_V2)
        collection_view = client.get_collection_view(
            url_or_id=my_secrets.MEMORIZATION_TIMES_TABLE_URL
        )

        for row in collection_view.collection.get_rows():
            date = row.date
            if len(date) > 13:
                date = date[:14]
            time = MemorizationTime(date=date, duration=row.time)
            if date:
                self.__memorization_times.append(time)
        self.__memorization_times.reverse()

    @property
    def memorization_times(self):
        """ Get memorization times which have dates (read-only) """
        return self.__memorization_times
