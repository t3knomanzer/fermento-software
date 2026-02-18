from time import localtime, time
from ntptime import settime


def setup_ntp_time():
    try:
        settime()
        print(f"Ntp time set. Current time {now_iso()} - {time()}")
        return True
    except Exception as e:
        print(f"Error setting ntp time. {e}")
        return False


def now():
    return localtime()


def now_iso():
    t = now()
    return "{:04d}-{:02d}-{:02d}T{:02d}:{:02d}:{:02d}Z".format(t[0], t[1], t[2], t[3], t[4], t[5])


def now_shortform():
    t = now()
    return "{:04d}-{:02d}-{:02d} {:02d}:{:02d}".format(t[0], t[1], t[2], t[3], t[4])


def iso_to_shortform(iso_str):
    result = iso_str.replace("T", " ")[:16]
    return result


def iso_to_int(dt_str: str) -> int:
    # "2026-02-18T15:10:22Z"
    return int(dt_str.replace("-", "").replace(":", "").replace("T", "").replace("Z", ""))


def ntp_is_set():
    # 5 minutes
    return time() > 3000
