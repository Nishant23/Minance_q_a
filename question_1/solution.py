import calendar

import datetime


def get_user_input():
    while 1:
        try:
            year = int(raw_input("Enter any year: "))
            return year
        except ValueError:
            print("Invalid Year")


def get_closest_leap_year(year):
    next_year = year + 1
    prev_year = year - 1
    while 1:
        if calendar.isleap(next_year):
            return next_year
        elif calendar.isleap(prev_year):
            return prev_year
        else:
            next_year += 1
            prev_year -= 1


def get_extra_day_date(year):
    extra_day = datetime.date(year, 2, 29).strftime('%A')
    return extra_day


def get_extra_day(year):
    leap_year = calendar.isleap(year)
    closest_year = year
    if not leap_year:
        closest_year = get_closest_leap_year(year)
    day = get_extra_day_date(closest_year)
    return leap_year, closest_year, day


def main():
    year = get_user_input()
    leap_year, closest_year, day = get_extra_day(year)

    if leap_year:
        print day
    else:
        print "This is not a leap year"
        print "Closest leap year: {0}".format(closest_year)
        print day


if __name__ == '__main__':
    main()
