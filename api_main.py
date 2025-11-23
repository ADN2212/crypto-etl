from flask import Flask, request
from api.compute_price_variation import compute_price_variation
from api.compute_price_avg import compute_price_avg
from api.compute_coin_liquidity import compute_coin_liquidity
from api.get_coin_data_in import get_coin_data_in
from dotenv import load_dotenv
from os import getenv

load_dotenv()

app = Flask(__name__)

#Calcula la variacion porcentual del precio en un intervalo dado:
@app.route("/compute-price-variation", methods=['GET'])
def compute_price_var():

    coin_name = request.args.get("coin-name")
    from_date = request.args.get('from-date')   
    until_date = request.args.get('until-date')
    
    return compute_price_variation(
        coin_name = coin_name,
        from_date_str = from_date, 
        until_date_str = until_date
    )

#Calcula el promedio del precio de una moneda en un intervalo dado:
@app.route("/compute-price-averege", methods=['GET'])
def compute_price_avgerage():
    
    coin_name = request.args.get("coin-name")
    from_date = request.args.get('from-date')   
    until_date = request.args.get('until-date')

    return compute_price_avg(
        coin_name = coin_name,
        from_date_str = from_date, 
        until_date_str = until_date
    )

#Calcula la liquidez media de una moneda en un dia dado:
@app.route("/compute-volume-to-market-cap-ratio", methods=['GET'])
def compute_liquidity():

    coin_name = request.args.get("coin-name")
    date = request.args.get('date')

    return compute_coin_liquidity(
        coin_name = coin_name,
        date_str = date
    )

#Da todos los datos de una moneda en un intervalo dado:
@app.route("/get-coin-data", methods=['GET'])
def get_coin_data():
    
    coin_name = request.args.get("coin-name")
    from_date = request.args.get('from-date')   
    until_date = request.args.get('until-date')

    return get_coin_data_in(
        coin_name = coin_name,
        from_date_str = from_date,
        until_date_str = until_date
    )


PORT = int(getenv("PORT"))

app.run(port = PORT, debug = True)
