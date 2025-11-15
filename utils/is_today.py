from datetime import datetime

def is_today(date: datetime) -> bool:
    today = datetime.today()
    return  today.year == date.year and today.month == date.month and today.day == date.day
