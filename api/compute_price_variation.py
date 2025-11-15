from datetime import datetime
from db.read_methods import get_price_from, get_price_until

# def parse_date(date_str: str) -> datetime:
#     y, m, d = date_str.split("-")
#     return datetime(
#         year = int(y),
#         month = int(m),
#         day = int(d)
#     )

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

    if from_date and not until_date:

        t2 = datetime.now()

        firts_price = get_price_from(
            coin_name = coin_name,
            start_date = from_date
            )
        
        last_price = get_price_until(
            coin_name = coin_name,
            end_date = datetime.now()
        )
        
        delta_time = t2 - from_date

        # print(firts_price)
        # print(last_price)
        # print(delta_time)

        if firts_price == None or last_price == None:
            return {
                "message": "no prices found"
            }

        variation_per_100 = round(((last_price - firts_price) / last_price) * 100, 3)

        return {
            "variation": f'{variation_per_100}%' ,
            "elapsed_time": {
                "days": delta_time.days,
                "hours": delta_time.seconds // 3600,
            }
        }
