import ntptime, time


def init_time():
    try:
        ntptime.settime()
        return True
    except:
        return False


def now():
    return time.localtime()


def now_str():
    t = time.localtime()
    return "{:04d}-{:02d}-{:02d} {:02d}:{:02d}:{:02d}".format(
        t[0], t[1], t[2], t[3], t[4], t[5]
    )


def ntp_is_set():
    # Any date after ~2020 is safe
    return time.time() > 1_600_000_000
