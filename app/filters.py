from datetime import datetime


def fldate(value):
    return datetime.utcfromtimestamp(value).strftime('%Y-%m-%d %H:%M:%S UTC')