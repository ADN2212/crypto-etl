from datetime import datetime

def is_more_than_today(date: datetime) -> bool:
    today = datetime.today()
    today_at_end = datetime(
                year=today.year, 
                month=today.month, 
                day=today.day,
                hour=23,
                minute=59,
                second=59
            )
    
    return date > today_at_end
