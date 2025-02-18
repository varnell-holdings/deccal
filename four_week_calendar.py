import calendar
import csv
from datetime import datetime, timedelta
import dateutil.easter
import os
import yaml

cal = calendar.Calendar()
# this gives us cal.itermonthdays2() which does the heavy lifting

START_DATE_STRING = "2024-10-01"  # this is a Tuesday

START_ROTATION = 3  # this is the rotation of the start date

WEEK_DICT = {0: "monday", 1: "tuesday", 2: "wednesday", 3: "thursday", 4: "friday"}

MONTH_DISPLAY = {1: "Jan_Mar", 4: "Apr_Jun", 7: "Jul_Sept", 10: "Oct_Dec"}

with open("timetable.yaml", "r") as f:
    TIMETABLE = yaml.safe_load(f)


def intro():
    def clear_screen():
        os.system("cls")

    clear_screen()

    hi = """Welcome to the dec calendar maker!
    This will generate a deccal.csv file for 3 months (trimester)
    which can be imported into google calendar.
    You will be asked to enter the year as 4 digits eg 2011
    Enter the start month of the trimester you want to add
    1: 'Jan_Mar', 4: 'Apr_Jun', 7: 'Jul_Sept', 10: 'Oct_Dec'

    """
    print(hi)

    while True:
        year = input("Year:  ")
        if year.isdigit() and len(year) == 4:
            break

    while True:
        start_month = input("Enter the start_month: ")
        if start_month in {"1", "4", "7", "10"}:
            break

    return int(year), int(start_month)


def last_week_flag_finder(month, year):
    """Finds the week_flag of the last day of the last trimester."""

    # get these dates into datetime objects
    start_date = datetime.strptime(START_DATE_STRING, "%Y-%m-%d")
    first_day_new_calendar = datetime.strptime(f"{year}-{month}-01", "%Y-%m-%d")

    last_day_old_calendar = first_day_new_calendar - timedelta(days=1)
    difference = last_day_old_calendar - start_date
    days_between = difference.days
    weeks_between = days_between // 7
    extra_days = days_between % 7

    # because Tuesday plus 6 goes to Monday - need an extra week flip
    if extra_days == 6:
        last_rotation = ((weeks_between + (START_ROTATION)) % 4) + 1
    else:
        last_rotation = ((weeks_between + (START_ROTATION - 1)) % 4) + 1

    return last_rotation  # ie flag of last week of last trimester


def is_holiday(day, month, year, weekday):
    easter_sunday = dateutil.easter.easter(year)
    easter_friday = easter_sunday - timedelta(days=2)
    easter_monday = easter_sunday + timedelta(days=1)
    # queens_birthday
    if month == 6 and weekday == 0 and day >= 8 and day <= 14:
        return True, "Queen's Birthday"
    # labour_day
    if month == 10 and weekday == 0 and day >= 1 and day <= 7:
        return True, "Labour Day"
    #  easter friday
    if month == easter_friday.month and day == easter_friday.day:
        return True, "Easter Friday"
    # easter monday
    if month == easter_monday.month and day == easter_monday.day:
        return True, "Easter Monday"
    # new years day
    if month == 1 and day == 1:
        return True, "New Year's Day"
    # australia day
    if month == 1 and day == 26:
        return True, "Australia Day"
    # anzac day
    elif month == 4 and day == 25:
        return True, "Anzac Day"
    # xmas and new year
    elif month == 12 and day in {25, 26, 27, 28, 29, 30, 31}:
        return True, "Xmas Holidays"
    else:
        return False, "Working Day"


def holiday_genenerator(year, start_month):
    """Yeilds tuples of holiday dates and names."""
    for month in range(start_month, start_month + 3):
        for monthday, weekday in cal.itermonthdays2(year, month):
            holiday, Subject = is_holiday(monthday, month, year, weekday)
            if holiday:
                yield "{}/{}/{}".format(monthday, month, year), Subject


def weekdays_gen(year, start_month):
    """Helper for trimester_with_week_flag_gen
    Yields a tuple of day of month, weekday number and month number
    for each weekday in trimester. Helper for trimester_with_week_flag_gen().
    cal.itermonthdays2 returns (day of month, weekday number)
    where 0 day of month means not in month and 0 weekday is Monday
    weekdays 5, 6 are Sat and Sun"""
    for month in range(start_month, start_month + 3):
        for monthday, weekday in cal.itermonthdays2(year, month):
            workday = monthday != 0 and weekday not in {5, 6}
            if workday:
                yield monthday, weekday, month


def trimester_with_week_flag_gen(year, week_flag, start_month):
    """Helper for write_calendar.
    Yields a tuple of  formatted date eg 1/2/2017
    and a string eg 'friday_3' which is the key to TIMETABLE representing
    day of week and week_flag"""

    def rotate_week(flag):
        """Move the week_flag one step thru the cycle 1,2,3,4,1..."""
        flag = flag % 4
        return flag + 1

    for monthday, weekday, month in weekdays_gen(year, start_month):
        if weekday == 0:
            week_flag = rotate_week(week_flag)
        yield (
            "{}/{}/{}".format(monthday, month, year),
            "{}_{}".format(WEEK_DICT[weekday], str(week_flag)),
        )


def write_calendar(year, week_flag, start_month):
    # 1.make initial cal_list:
    cal_list = []
    for date, key in trimester_with_week_flag_gen(year, week_flag, start_month):
        for event in TIMETABLE[key]:
            entry = event[0], date, event[1], False, event[2]
            cal_list.append(entry)

    # 2.make holiday dictionary date:holiday_title (Google uses 'Subject')
    hol_dict = {
        date: Subject for (date, Subject) in holiday_genenerator(year, start_month)
    }
    # 3. remove holidays from cal_list
    cal_list = [lis for lis in cal_list if lis[1] not in hol_dict]

    # 4.write cal_list to csv
    headers = ("Subject", "Start Date", "Start Time", "All Day Event", "Location")
    address = f"{year}_{MONTH_DISPLAY[start_month]}.csv"
    with open(address, "w") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        for i in cal_list:
            writer.writerow(i)
        # 5.now write in holidays - must do this last
        for date, Subject in hol_dict.items():
            entry = Subject, date, "", True, "Both Rooms"
            writer.writerow(entry)

    print("\nSuccess!\nYou can now import the csv file.\n")
    input("\nPress Enter to close this screen:")


def main():
    year, start_month = intro()
    week_flag = last_week_flag_finder(start_month, year)
    write_calendar(year, week_flag, start_month)


if __name__ == "__main__":
    main()
