from time import localtime, time
from ntptime import settime


def setup_ntp_time():
    try:
        settime()
        print(f"Ntp time set. Current time {now_str()} - {time()}")
        return True
    except Exception as e:
        print(f"Error setting ntp time. {e}")
        return False


def now():
    return localtime()


def now_str():
    t = localtime()
    return "{:04d}-{:02d}-{:02d} {:02d}:{:02d}:{:02d}".format(t[0], t[1], t[2], t[3], t[4], t[5])


def ntp_is_set():
    # 5 minutes
    return time() > 3000
