from son.gameplay._types import TurnInfo

# Constants for the month names
_MONTHS = [
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December"
]


class TurnTracker:
    """
    Turn tracker that keeps track of the current turn.

    The turns are calendar based:
        - each year is 12 months
        - each month is 4 weeks
        - 1 week is 1 turn
    """

    def __init__(self):
        self._week: int = 1
        self._month: int = 0
        self._year: int = 1

    def skip_turn(self):
        """
        Skip 1 turn and update the tracker.
        """
        self._week += 1

        if self._week > 4:
            self._week = 1
            self._month += 1

        if self._month > 11:
            self._month = 0
            self._year += 1

    @property
    def turn_info(self):
        """
        Info about the current turn.
        """
        return TurnInfo(
            week=str(self._week),
            month=_MONTHS[self._month],
            year=str(self._year)
        )
