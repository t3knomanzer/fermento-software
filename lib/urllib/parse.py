from ure import compile as _re_compile


# Minimal URL encoder for MicroPython (spaces + a few specials)
def quote(s, safe=""):
    hexmap = "0123456789ABCDEF"
    out = []
    for ch in s:
        o = ord(ch)
        if ("a" <= ch <= "z") or ("A" <= ch <= "Z") or ("0" <= ch <= "9") or ch in safe:
            out.append(ch)
        else:
            out.append("%" + hexmap[(o >> 4) & 0xF] + hexmap[o & 0xF])
    return "".join(out)


def urlencode(params):
    # params: list of (key, value) to preserve order / allow duplicates
    parts = []
    for k, v in params:
        parts.append("{}={}".format(quote(str(k), safe="[]"), quote(str(v))))
    return "&".join(parts)
