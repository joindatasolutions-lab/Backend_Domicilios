from datetime import date, datetime
from zoneinfo import ZoneInfo


LOCAL_TIMEZONE = ZoneInfo("America/Bogota")


def today_local() -> date:
    return datetime.now(LOCAL_TIMEZONE).date()
