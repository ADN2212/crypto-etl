# Crypto ETL

This application is composed of two main parts: a scraper responsible for extracting data from [CoinMarketCap](https://coinmarketcap.com/), and an API that exposes multiple endpoints powered by that data.
The main goal of the project is to generate useful insights from the information collected by the scraper.

## Technologies Used

- **BeautifulSoup**  
  Used for parsing and extracting structured data from HTML pages during the scraping process.

- **SQLAlchemy**  
  Serves as the ORM layer to manage database models, handle queries, and interact cleanly with PostgreSQL.

- **Flask**  
  Powers the API layer, providing endpoints that expose the scraped and processed data.

- **PostgreSQL**  
  The main relational database used to store the collected data and support efficient querying.

- **Python `datetime`**  
  Utilized for handling dates and times.

## Endpoints

- **GET //compute-price-variation**  
  Accepts `coin-name`, `from-date`, and `until-date` as query parameters and calculates the price variation of the specified coin within the given time range.  
  - If only `from-date` is provided, the response returns the price variation from that date up to the present.  
  - If only `until-date` is provided, the response returns the variation from the coin’s earliest recorded entry in the database up to the given date.

```json
"Example response body:"
{
    "variation": "5.67 %",
    "elapsed_time": {
        "days": 7,
        "hours": 15
    }
}
```

- **GET //compute-price-averege**  
  Accepts `coin-name`, `from-date`, and `until-date` as query parameters and calculates the price average within the given time range.  

```json
"Example response body:"
{
    "average_price": 1500.75,
}
```

- **GET //compute-volume-to-market-cap-ratio**  
  Accepts `coin-name`, `date` as query parameters and calculates the liquidity of the coin in the day given by the day.

```json
"Example response body:"
{
    "liquidity": "13.5 %",
}
```

- **GET //get-coin-data**  
  Accepts `coin-name`, `from-date`, and `until-date` as query parameters and returs all the stored data of the coin that was stored in the given interva.

```json

"Example response body:"
{
    "complete me"
}
```

## Usage

Make sure that you have the latest Python version installed and set up a virtual environment before installing the project dependencies.

### 1. Create and activate a virtual environment

```bash
# Create a virtual environment (recommended name: venv)
python -m venv venv

# Activate it on Linux / macOS
source venv/bin/activate

# Activate it on Windows
venv\Scripts\activate

# Intall dependencies
pip install -r requirements.txt

#For runing the scraper
python scraper_main.py

#For runing the api
python api_main.py
```

And then you are ready 🚀
