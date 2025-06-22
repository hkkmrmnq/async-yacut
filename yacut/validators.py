import re


def valid_short_id(short_id):
    pattern = r'^[A-Za-z0-9]{1,16}$'
    return re.match(pattern, short_id)
