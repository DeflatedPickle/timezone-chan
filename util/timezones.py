from collections import defaultdict
from datetime import datetime
from zoneinfo import available_timezones, ZoneInfo


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
    return [f"UTC{'+' if i >= 0 else ''}{i}" for i in range(-12, +12 + 1)]




