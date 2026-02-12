import time
from ntptime import settime


def setup_ntp_time():
    try:
        settime()
        print(f"Ntp time set. Current time {now_isoformat()} - {time.time()}")
        return True
    except Exception as e:
        print(f"Error setting ntp time. {e}")
        return False


def now():
    return time.localtime()


def now_isoformat():
    return time.strftime("%Y-%m-%dT%H:%M:%S%z", now())


def ntp_is_set():
    # 5 minutes
    return time.time() > 300
