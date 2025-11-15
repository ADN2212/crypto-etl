from flask import Flask, request
from api.compute_price_variation import compute_price_variation


app = Flask(__name__)

@app.route("/compute-price-variation", methods=['GET'])
def compute_price_var():
    #print(request.args.get("a"))

    coin_name = request.args.get("coin-name")
    from_date = request.args.get('from-date')   
    until_date = request.args.get('until-date')

    print(coin_name)
    print(from_date)
    print(until_date)

    return compute_price_variation(
        coin_name = coin_name,
        from_date_str = from_date, 
        until_date_str = until_date
    )

app.run(port=8080, debug=True)
