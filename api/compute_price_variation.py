from datetime import datetime
from db.methods import get_price_from, get_price_until, get_min_date_for_coin
from utils.is_today import is_today
from utils.is_more_than_today import is_more_than_today
from utils.last_day_moment import last_day_momonet

from flask import Response

def compute_price_variation(coin_name: str | None, from_date_str = str | None, until_date_str = str | None):

    if coin_name == None:
        return Response(
            response = str({"message": "A coin name must be provided"}),
            status = 400
        )
    
    try:
        from_date = datetime.fromisoformat(from_date_str) if from_date_str != None else None
        until_date = datetime.fromisoformat(until_date_str) if until_date_str != None else None
    except ValueError:
        return Response(
            response = str({"message": "No valid format for date"}),
            status = 400
        )
    
    if is_more_than_today(from_date) or is_more_than_today(until_date):
        return Response(
            response= str({"message": "Dates can not be more than the current day"}),
            status = 400
        )

    t1 = None
    t2 = None

    if from_date and until_date == None:
        t1 = from_date
        t2 = datetime.now()
    
    if from_date == None and until_date:
        t1 = get_min_date_for_coin(coin_name = coin_name)
        if is_today(until_date):
            t2 =  datetime.now()
        else:
            t2 = last_day_momonet(until_date)

    if from_date and until_date:
        if from_date >= until_date:
            return Response(
                response = str({"message": "from_date must be less than until_date"}),
                status = 400
            )
        
        t1 = from_date
        if is_today(until_date):
            t2 =  datetime.now()
        else:
            t2 = last_day_momonet(until_date)

    firts_price = get_price_from(coin_name = coin_name, start_date = t1)
    last_price = get_price_until(coin_name = coin_name, end_date = t2)
        
    delta_time = t2 - t1

    if firts_price == None or last_price == None:
        return Response(
            response = str({"message": "no prices found"}),
            status = 404
        )

    variation_per_100 = round(((last_price - firts_price) / last_price) * 100, 3)

    return Response(
        response = str({
        "variation": f'{variation_per_100} %',
        "elapsed_time": {
            "days": delta_time.days,
            "hours": round(delta_time.seconds / 3600, 2)}
            }
        ),
        status = 200
    )
