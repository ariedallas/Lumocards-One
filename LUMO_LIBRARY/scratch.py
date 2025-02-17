import calendar
import datetime
import time

from dateutil.relativedelta import relativedelta
from pprint import pprint as pp

def get_nearest_monday(dt):
    amt = dt.weekday()
    return dt - relativedelta(days=amt)

def get_datetimes_for_iso_week(iso_week):
    print(iso_week)


def function_timer(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()

        print(func.__name__)
        print(end - start)
        return result

    return wrapper

dt = datetime.date(year=2025, month=2, day=15)
print(f"ORIG DT: {dt}")
dt_start = get_nearest_monday(dt)
print(f"NEAR MONDAY: {dt_start}")

iso_week = dt_start.isocalendar()[1]
print(f"ISO WEEK: {iso_week}")

def get_timeframe(var_date):
    nearest_monday = get_nearest_monday(var_date)
    start_of_day_blocks = nearest_monday - relativedelta(days=42)
    end_of_day_blocks = start_of_day_blocks + relativedelta(days=90)

    return start_of_day_blocks, end_of_day_blocks

def generate_day_blocks(var_date):
    nearest_monday = get_nearest_monday(var_date)
    start_of_day_blocks = nearest_monday - relativedelta(days=42)

    dayblocks = []
    for d in range(91):
        next_day = start_of_day_blocks + relativedelta(days=d)
        dayblocks.append(next_day)

    return dayblocks

def separate_by_weeks(dayblocks):
    separated_weeks = []
    num_weeks = round(len(dayblocks) / 7)
    for x in range(num_weeks):
        start = 7 * x
        end = (7 * x) + 7
        separated_weeks.append(dayblocks[start: end])

    return separated_weeks

# dayblocks = generate_day_blocks(dt)
# sep = separate_by_weeks(dayblocks)

li = list(range(13))
print(li)

base = li[:-4]
print(base)

