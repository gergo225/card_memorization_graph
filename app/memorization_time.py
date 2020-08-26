""" MemorizationTime class """
import datetime


class MemorizationTime:
    """ Holds the date and the duration
    of a memorization

    Attributes
    ----------
    date : datetime
        When was the memorization recorded
        Returns '-' when undefined
    duration : datetime.timedelta
        How much time it took to memorize
    """

    def __init__(self, date: str, duration: str):
        self.__date = date
        if date:
            year = int(date[:4])
            month = int(date[6:8])
            day = int(date[10:12])
            self.__date = datetime.datetime(year, month, day)

        minutes = int(duration[:-3])
        seconds = int(duration[-2:])
        self.__duration = datetime.timedelta(minutes=minutes, seconds=seconds)

    @property
    def date(self):
        """ The date of the memorization (read-only)

        Format: yyyy-MM-dd"""
        if not self.__date:
            return "-"
        return str(self.__date)[:-9]

    @property
    def duration(self):
        """ How much time it took to memorize (read-only)

        Format: mm:ss """
        return str(self.__duration)[2:]
