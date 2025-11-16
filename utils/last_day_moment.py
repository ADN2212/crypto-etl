from datetime import datetime

def last_day_momonet(date: datetime) -> datetime:
    return datetime(
                year=date.year, 
                month=date.month, 
                day=date.day,
                hour=23,
                minute=59,
                second=59,
                microsecond=999999
            )
