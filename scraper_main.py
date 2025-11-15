from time import localtime, sleep
from datetime import datetime
from bs4 import BeautifulSoup
from requests import get
from requests.exceptions import ConnectionError
from db.engine import init_data_base, crypto_data_table
from sqlalchemy import insert
from utils.parse_to_float import parse_to_float
from dotenv import load_dotenv 
from os import getenv

load_dotenv()

#It make sence ?
SURCE_URL = getenv("SOURCE_URL")
TIME_TO_WAIT = int(getenv("TIME_TO_WAIT"))

def extract_data():
    now = localtime()
    print(f"Scraping Coinmarketcap at min = {now.tm_min}, hour = {now.tm_hour}, day = {now.tm_mday}")
    
    try:
        response = get(SURCE_URL)
    except ConnectionError:
        return []
    
    soup = BeautifulSoup(response.text, 'html.parser')
    rows = soup.find_all('tr')[0:11]#Just the firts ten entries ...
    
    if len(rows) == 0:
        return []
    
    coins_data = []
    curr_cells_list = None

    for row in rows:
        curr_cells_list = row.find_all("td")
        if len(curr_cells_list) >= 8:
            coins_data.append(
                {
                    "coin_name": curr_cells_list[2].find(attrs={"class": "coin-item-name"}).text,
                    "price": parse_to_float(curr_cells_list[3].text),
                    "market_cap": parse_to_float(curr_cells_list[7].text.split("$")[2]),#it is better to find a way to get the second span from BS
                    "volume_24": parse_to_float(curr_cells_list[8].find("p").text),
                    "scraped_at": datetime.now()
                }
            )

    return coins_data

#TODO:put this into a constants folder


if __name__ == "__main__":

    db = init_data_base()
    
    if db == False:
        print("An error ocurred while trying to connect to the data base.")
    else:
        while True:     
            data = extract_data()
            if len(data) != 0:
                #Esto es una transaccion, ademas abre y cierra la conexion a lo largo del bloque with
                with db.connect() as conn:
                    conn.execute(insert(crypto_data_table), data)            
                    conn.commit()
                    print("Data collected succesfully, waiting 5 minutes ...")
                sleep(TIME_TO_WAIT)
            else:
                print("The data could not be fetched")
                break
