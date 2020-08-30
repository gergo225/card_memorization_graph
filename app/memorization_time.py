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
        return str(self.__date)[:-9]

    @property
    def serial_date(self):
        """ The date represented by a serial number which is used to
        add a new value to a cell in a spreadsheet (read-only) """
        anchor_date = datetime.datetime(1899, 12, 30)
        days_since_anchor = self.__date - anchor_date
        return days_since_anchor.days

    @property
    def duration(self):
        """ How much time it took to memorize (read-only)

        Format: mm:ss """
        return str(self.__duration)[2:]

    @property
    def serial_duration(self):
        """ The duration of the memorization represented by serial number
        which is used when adding a new value to a spreadsheet cell (read-only) """
        seconds = 0.000011574
        duration = self.__duration.seconds * seconds
        return round(duration, 9)
