from flask import Response
from datetime import datetime
from db.methods import compute_avg_in_interval
from utils.is_today import is_today
from utils.is_more_than_today import is_more_than_today
from utils.last_day_moment import last_day_momonet

def compute_price_avg(coin_name: str | None, from_date_str = str | None, until_date_str = str | None) -> Response:

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

    if from_date == None or until_date == None:
        return Response(
            response = str({"message": "both dates must be provided"}),
            status = 400
        )
    
    if is_more_than_today(from_date) or is_more_than_today(until_date):
        return Response(
            response= str({"message": "Dates can not be more than the current day"}),
            status = 400
        )
    
    
    if from_date >= until_date:
        return Response(
            response = str({"message": "from_date must be less than until_date"}),
            status = 400
        )

    t2 = None

    if is_today(until_date):
        t2 =  datetime.now()
    else:
        t2 = last_day_momonet(until_date)

    avg = compute_avg_in_interval(
        coin_name = coin_name,
        start_date = from_date,
        end_date = t2
    )    

    if avg == None:
        return Response(
            response = str({"message": "No data found"}),
            status = 404
        )

    return Response(
        response=str({
            "average_price": avg,
        }),
        status = 200
    )
