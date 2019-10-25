SECONDS_PER_HOUR = 60 * 60
SECONDS_PER_DAY = SECONDS_PER_HOUR * 24
SECONDS_PER_WEEK = SECONDS_PER_DAY * 7

def datetime_to_hour(datetime):
    hours = int(datetime.timestamp() / SECONDS_PER_HOUR)
    return hours * SECONDS_PER_HOUR
