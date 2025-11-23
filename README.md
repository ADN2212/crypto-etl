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
    "variation": "-0.197 %", 
    "elapsed_time": {
        "days": 2, 
        "hours": 24.0
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
  "data": [
        {
          "price": 95456.51, 
          "market_cap": 1901427690511.0, 
          "volume_24": 112344817780.0
        },
        {
          "price": 95572.74, 
          "market_cap": 1906596319698.0, 
          "volume_24": 107741187183.0
        },
        {
          "price": 96331.06, 
          "market_cap": 1921155625906.0, 
          "volume_24": 79900390495.0
        },
        {
          "price": 99241.34, 
          "market_cap": 1980634554974.0, 
          "volume_24": 104653100236.0
        }
      ]
}
```

## Usage
In order to use this project folow the next steps:

### 1. Set up the env vars
```
TIME_TO_WAIT=The amount of time in seconds that the scraper will wait to extact the data
SOURCE_URL=https://coinmarketcap.com/
DATA_BASE_URL=The direction of your data base
PORT=The port that will serves the API (usually 8080)
```
### 2. Create a virtual environment and activate it (recommended name: crypto_etl)
```bash
python -m venv crypto_etl

# Activate it on Linux / macOS
source venv/bin/activate

# Activate it on Windows
venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt #this is the one in this repository
```

### 4. Run de scraper and leave it some time extracting data
```bash
python scraper_main.py
``` 

### 5. Finally you can run de api to use the endpoints previously descrived
```bash
python api_main.py
```

## And then you are ready 🚀