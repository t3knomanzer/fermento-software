from time import localtime, time
from ntptime import settime


def init_time():
    try:
        settime()
        return True
    except:
        return False


def now():
    return localtime()


def now_str():
    t = localtime()
    return "{:04d}-{:02d}-{:02d} {:02d}:{:02d}:{:02d}".format(
        t[0], t[1], t[2], t[3], t[4], t[5]
    )


def ntp_is_set():
    # Any date after ~2020 is safe
    return time() > 1_600_000_000
