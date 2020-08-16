import datetime
from django.utils import timezone

# Convert stringified date to an interger turple
def int_date(str_date): # string fields need to be seperated by dash "2020-04-17"
	date_fields = str_date.split("-")
	# Convert each field to interger
	for i in range(len(date_fields)):
		date_fields[i] = int(date_fields[i])
	return tuple(date_fields)

# Return 1 to 7 based on the day
def week_day(date):
	return (int(date.strftime("%w"))-1)%7+1

# Return the current week 
def current_week():
	return int(timezone.now().date().strftime('%W'))

def current_day():
    return int(timezone.now().date().strftime('%d'))

def current_month():
    return int(timezone.now().date().strftime('%m'))

def current_year():
    return int(timezone.now().date().strftime('%Y'))

# Get the date for a specific week day
def current_week_dates(year, week, day):
	# https://stackoverflow.com/questions/396913/in-python-how-do-i-find-the-date-of-the-first-monday-of-a-given-week
    date = datetime.date(year, 1, 4) 
    return date + datetime.timedelta(weeks=week, days=-date.weekday()+day-1)

# Date class
class Date:
    def now(self):
        return timezone.now().date()

    def week(self):
        return current_week()

    def day(self):
        return current_day()

    def month(self):
        return current_month()

    def year(self):
        return current_year()

# Custom error
class CustomError(Exception):
    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self):
        if self.message:
            return f'ERROR: {self.message}'
        else:
            return "ERROR"
