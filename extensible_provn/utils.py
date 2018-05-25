import dateutil.parser

def unquote(value):
    if value and value.startswith('"'):
        value = value[1:-1]
    return value

def parsetime(time):
    time = unquote(time)
    if time and time.startswith("T") and time[1:].isdigit():
        return int(time[1:])
    elif time and time.isdigit():
        return int(time)
    try:
        return dateutil.parser.parse(time) if time else None
    except ValueError:
        return None
