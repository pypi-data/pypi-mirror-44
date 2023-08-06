import datetime
import time

def day_and_hour(d, h):
    """Counts down to a set day and time from current time"""
    days_to_numbers = [['monday', 0],
                       ['tuesday', 1],
                       ['wednesday', 2],
                       ['thursday', 3],
                       ['friday', 4],
                       ['saturday', 5],
                       ['sunday', 6]]

    for i in days_to_numbers:
        if d == i[0]:
            number_wanted_day = i[1]

    today = datetime.datetime.today().weekday()
    delta_days = (number_wanted_day - today) % 7
    actual_time = time.localtime(time.time())

    if h > actual_time[3]:
        delta_hours = h - actual_time[3]
        delta_mins = 59 - actual_time[4]
        delta_secs = 59 - actual_time[5]
    else:
        delta_days = delta_days - 1
        delta_hours = 23 - actual_time[3] + h
        delta_mins = 59 - actual_time[4]
        delta_secs = 59 - actual_time[5]

    return [delta_days, delta_hours, delta_mins, delta_secs]

def hour(h):
    """Counts down to a set time every day"""
    now = int(datetime.datetime.now().strftime("%H"))
    delta_hours = (h - now) % 24
    actual_time = time.localtime(time.time())

    if h > actual_time[3]:
        delta_hours = h - actual_time[3]
        delta_mins = 59 - actual_time[4]
        delta_secs = 59 - actual_time[5]
    else:
        delta_hours = 23 - actual_time[3] + h
        delta_mins = 59 - actual_time[4]
        delta_secs = 59 - actual_time[5]

    return [delta_hours, delta_mins, delta_secs]
    