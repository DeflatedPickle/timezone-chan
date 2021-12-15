import re
from collections import defaultdict
from datetime import datetime
from zoneinfo import available_timezones, ZoneInfo

from discord import Member, Guild, Role


def gather_timezones():
    now = datetime.now()
    tz_map = defaultdict(list)

    for tz in available_timezones():
        zone = ZoneInfo(tz).tzname(now)

        if zone.isalpha():
            tz_map[zone].append(tz)

    return {k: sorted(v) for k, v in tz_map.items()}


def gather_places(continent: str):
    l = []

    for tz in available_timezones():
        if continent.lower() in tz.lower():
            l.append(tz)

    return sorted(l)


def gather_utc():
    # str(i).zfill(2)
    return [f"UTC{'+' if i >= 0 else ''}{i}" for i in range(-12, +12 + 1)]


def is_timezone_role(role: Role):
    m = re.findall(r"\d{1,2}", role.name)

    if m:
        c = re.split("[+-]", role.name)[0] + \
            re.findall("[+-]", role.name)[0] + \
            re.findall(r"\d{1,2}", role.name)[0].zfill(2)
        return re.search("UTC[+-](0[0-9]|1[0-2])", c) is not None
    else:
        return False


def get_timezone_role(member: Member):
    for i in member.roles:
        if is_timezone_role(i):
            return i
    return None


def same_timezone(you: Member, other: Member):
    yt = get_timezone_role(you)
    ot = get_timezone_role(other)

    if yt is None or ot is None: return
    return yt.name == ot.name


def timezone_difference(you: Member, other: Member):
    yt = get_timezone_role(you)
    ot = get_timezone_role(other)

    if yt is None or ot is None: return

    ytn = int(re.findall(r"[+-]\d{1,2}", yt.name)[0])
    otn = int(re.findall(r"[+-]\d{1,2}", ot.name)[0])

    if ytn < otn:
        p = "+"
    else:
        p = "-"

    if ytn <= 0 and otn <= 0:
        m = min(ytn, otn) - max(ytn, otn)
    else:
        m = max(ytn, otn) - min(ytn, otn)

    return m
