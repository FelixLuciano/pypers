import datetime


_now = datetime.datetime.now()
_MONTHS = (None, "January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December")

day = str(_now.day)
day += "st" if _now.day == 1 else "nd" if _now.day == 2 else "th"

month = _MONTHS[_now.month]
year = _now.year
