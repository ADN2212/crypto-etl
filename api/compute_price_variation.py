from datetime import datetime
from db.read_methods import get_price_from, get_price_until, get_min_date_for_coin

#Tal vez en un archivo de constantes ???
#MIN_DATE = datetime(year=MINYEAR, month=1, day=1)

def is_today(date: datetime) -> bool:
    now = datetime.today()
    return  now.year == date.year and now.month == date.month and now.day == date.day
 
def compute_price_variation(coin_name: str | None, from_date_str = str | None, until_date_str = str | None):

    if coin_name == None:
        return {
            "message": "A coin name must be provided"
        }

    try:
        from_date = datetime.fromisoformat(from_date_str) if from_date_str != None else None
        until_date = datetime.fromisoformat(until_date_str) if until_date_str != None else None
    except ValueError:
        #TODO: sed a Bad Request response code
        return {
            "message": "No valid format for date"
        }

    t1 = None
    t2 = None

    if from_date and until_date == None:
        print("Case one")
        t1 = from_date
        t2 = datetime.now()
    
    if from_date == None and until_date:
        print("case 2")
        t1 = get_min_date_for_coin(coin_name = coin_name)
        if is_today(until_date):
            t2 =  datetime.now()
        else:
            t2 = datetime(
                year=until_date.year, 
                month=until_date.month, 
                day=until_date.day,
                hour=23,
                minute=59,
                second=59
            )

    if from_date and until_date:
        print("Case 3")
        t1 = from_date
        t2 = until_date

    firts_price = get_price_from(coin_name = coin_name, start_date = t1)
    last_price = get_price_until(coin_name = coin_name, end_date = t2)
        
    delta_time = t2 - t1

    if firts_price == None or last_price == None:
        return {
            "message": "no prices found"
        }

    variation_per_100 = round(((last_price - firts_price) / last_price) * 100, 3)

    return {
        "variation": f'{variation_per_100} %',
        "elapsed_time": {
            "days": delta_time.days,
            "hours": round(delta_time.seconds / 3600, 2),
            }
        }
