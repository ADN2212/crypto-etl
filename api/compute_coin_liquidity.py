from flask import Response
from datetime import datetime
from utils.is_more_than_today import is_more_than_today
from utils.last_day_moment import last_day_momonet
from db.methods import compute_volue_market_cap_ratio

def compute_coin_liquidity(coin_name: str | None, date_str = str | None) -> Response:

    if coin_name == None:
        return Response(
            response = str({"message": "A coin name must be provided"}),
            status = 400
        )
    
    if date_str == None:
        return Response(
            response = str({"message" : "A date must be provided"})
        )

    try:
        date = datetime.fromisoformat(date_str) if date_str != None else None
    except ValueError:
        return Response(
            response = str({"message": "No valid format for date"}),
            status = 400
        )

    if is_more_than_today(date):
        return Response(
            response= str({"message": "Dates can not be more than the current day"}),
            status = 400
        )        

    liquidity = compute_volue_market_cap_ratio(
        coin_name = coin_name,
        start_date = date,
        end_date = last_day_momonet(date)
    )

    if liquidity == None:
        return Response(
            response = str({"message" : "No data found"}),
            status = 400
        )

    return Response(
        response = str({"liquidity": f'{ round(liquidity * 100, 3)} %'}),
        status = 200
    )
