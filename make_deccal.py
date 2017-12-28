import calendar
import csv
import datetime
import dateutil.easter

import colorama

cal = calendar.Calendar()


TIMETABLE = {
    'monday_a': [['Feller/Bowring', '07:30 AM', 'Room 1'], ['Bariol/Tillett', '07:30 AM', 'Room 2'], ['Rotation/Bowring', '01:30 PM', 'Room 1'], ['Meagher/Tillett', '1:30 PM', 'Room 2'], ],
    'monday_b': [['Feller/Brown', '07:30 AM', 'Room 1'], ['Bariol/Tillett', '07:30 AM', 'Room 2'], ['Rotation/Brown', '01:30 PM', 'Room 1'], ['Meagher/Tillett', '1:30 PM', 'Room 2'], ],
    'tuesday_a': [['Wettstein/Tillett', '07:30 AM', 'Room 1'], ['Stoita/Vuong', '07:30 AM', 'Room 2'], ['Danta/Tillett', '01:30 PM', 'Room 1'], ['Gett/Tester', '1:30 PM', 'Room 2'], ],
    'tuesday_b': [['Wettstein/Tillett', '07:30 AM', 'Room 1'], ['Stoita/Vuong', '07:30 AM', 'Room 2'], ['Danta/Tillett', '01:30 PM', 'Room 1'], ['Gett/Tester', '1:30 PM', 'Room 2'], ],
    'wednesday_a': [['Wettstein/Tillett', '07:30 AM', 'Room 1'], ['Vickers/Riley', '07:30 AM', 'Room 2'], ['Williams/Tillett', '01:30 PM', 'Room 1'], ['Ghaly/Riley', '1:30 PM', 'Room 2'], ],
    'wednesday_b': [['Wettstein/Tillett', '07:30 AM', 'Room 1'], ['Vickers/Riley', '07:30 AM', 'Room 2'], ['Free/Tillett', '01:30 PM', 'Room 1'], ['Ghaly/Riley', '1:30 PM', 'Room 2'], ],
    'thursday_a': [['Feller/Tillett', '07:30 AM', 'Room 1'], ['Stoita/Stevens', '07:30 AM', 'Room 2'], ['Meagher/Tillett', '01:00 PM', 'Room 1'], ['Williams/Stevens', '1:30 PM', 'Room 2'], ],
    'thursday_b': [['Feller/Tillett', '07:30 AM', 'Room 1'], ['Stoita/Brown', '07:30 AM', 'Room 2'], ['Meagher/Tillett', '01:00 PM', 'Room 1'], ['Williams/Brown', '1:30 PM', 'Room 2'], ],
    'friday_a': [['Vickers/Tillett', '07:30 AM', 'Room 1'], ["Suhirdan/O'Sullivan", '07:30 AM', 'Room 2'], ['Meagher/Tillett', '01:30 PM', 'Room 1'], ["Ghaly/O'Sullivan", '1:30 PM', 'Room 2'], ],
    'friday_b': [['Vickers/Tillett', '07:30 AM', 'Room 1'], ['Suhirdan/Vuong', '07:30 AM', 'Room 2'], ['Lord/Tillett', '01:30 PM', 'Room 1'], ['Ghaly/Vuong', '1:30 PM', 'Room 2'], ],
}


week_dict = {0: 'monday', 1: 'tuesday', 2: 'wednesday', 3: 'thursday', 4: 'friday'}


def is_holiday(day, month, year, weekday):
    easter_sunday = dateutil.easter.easter(year)
    easter_friday = easter_sunday - datetime.timedelta(days=2)
    easter_monday = easter_sunday + datetime.timedelta(days=1)
    # queens_birthday
    if month == 6 and weekday == 0 and day >= 8 and day <= 14:
        return True, "Queen's Birthday"
    # labour_day
    if month == 10 and weekday == 0 and day >= 1 and day <= 7:
        return True, 'Labour Day'
    #  easter friday
    if month == easter_friday.month and day == easter_friday.day:
        return True, 'Easter Friday'
    # easter monday
    if month == easter_monday.month and day == easter_monday.day:
        return True, 'Easter Monday'
    # new years day
    if month == 1 and day in{1}:
        return True, "New Year's Day"
    # australia day
    if month == 1 and day in {26}:
        return True, 'Australia Day'
    # anzac day
    elif month == 4 and day in {25}:
        return True, 'Anzac Day'
    # xmas and new year
    elif month == 12 and day in {25, 26, 27, 28, 29, 30, 31}:
        return True, 'Xmas Holidays'
    else:
        return False, 'Working Day'


def flip_week(flag):
    if flag == 'a':
        return 'b'
    else:
        return 'a'


# itermonthdays2 returns (day of month, weekday number)
# where 0 day of month means not in month and 0 weekday is Monday
def year_gen(year):
    """Yields a tuple of day of month, weekday number and month number."""
    for month in range(1, 13):
        for monthday, weekday in cal.itermonthdays2(year, month):
            workday = monthday != 0 and weekday not in {5, 6}
            if workday and not is_holiday(monthday, month, year, weekday)[0]:
                yield monthday, weekday, month


def holiday_gen(year):
    for month in range(1, 13):
        for monthday, weekday in cal.itermonthdays2(year, month):
            holiday, Subject = is_holiday(monthday, month, year, weekday)
            if holiday:
                yield '{}/{}/{}'.format(monthday, month, year), Subject


def year_with_week_flag_gen(year, week_flag):
    """Yields a tuple of  formatted date eg 1/2/2017
        and a string eg fridayb as key to TIMETABLE representing
        day of week and week_flag"""
    for monthday, weekday, month in year_gen(year):
        if weekday == 0:
            week_flag = flip_week(week_flag)
        yield ('{}/{}/{}'.format(monthday, month, year),
               '{}_{}'.format(week_dict[weekday], week_flag))


def clear():
    print('\033[2J')  # clear screen
    print('\033[1;1H')  # move to top left


def intro():
    colorama.init(autoreset=True)
    clear()

    hi = """Welcome to the dec calendar maker!
    This will generate a deccal.csv file which can be imported
    into google calendar.
    You will be asked to enter the year as 4 digits eg 2011
    and the roster of last day of previous year
    where a is the Bowring/Stevens week and b is the Campbell Brown week.
    To modify the roster, open deccal.py in a text editor and modify TIMETABLE,
    which is near the top of the file.

    """
    print(hi)
    while True:
        year = input('Year:  ')
        if year.isdigit() and len(year) == 4:
            year = int(year)
            break
    while True:
        week_flag = input('Enter a or b: ')
        if week_flag in {'a', 'b'}:
            break
    return year, week_flag


def write_cal(year, week_flag):
    with open('deccal.csv', 'r') as f:
        file = f.readline()
        headers = file.strip().split(',')
        headers = tuple(headers)
    with open('deccal.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        for date, key in year_with_week_flag_gen(year, week_flag):
            for event in TIMETABLE[key]:
                entry = event[0], date, event[1], False, event[2]
                writer.writerow(entry)
        for date, Subject in holiday_gen(year):
            entry = Subject, date, '', True, 'Both Rooms'
            writer.writerow(entry)
        print('\nSuccess!\nYou can now import deccal.csv '
              'which is in the same directory as this program.\n')


if __name__ == '__main__':
    year, week_flag = intro()
    write_cal(year, week_flag)
