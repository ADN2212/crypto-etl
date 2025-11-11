from time import localtime, sleep
from bs4 import BeautifulSoup
import requests

#TODO:Crear una carpeta de DTOs para esta y otras classes ?
class CoinData():
    def __init__(self, name, price, market_cap, volume_24):
        self.name = name
        self.price = price
        self.market_cap = market_cap
        self.volume_24 = volume_24
        now = localtime()
        self.date = f'{now.tm_min}:{now.tm_hour}:{now.tm_mday}:{now.tm_mon}:{now.tm_year}'
    
    def __str__(self):
        return f'CoinData({self.name}, {self.price}, {self.date})'

def main():
    now = localtime()
    print(f"Scraping Coinmarketcap at min = {now.tm_min}, hour = {now.tm_hour}, day = {now.tm_mday}")
    #TODO: handle posible errors:
    response = requests.get("https://coinmarketcap.com/")
    soup = BeautifulSoup(response.text, 'html.parser')
    rows = soup.find_all('tr')[0:11]  
    
    if len(rows) == 0:
        print("No rows where found")
        return
    
    coins_data = []
    curr_cells_list = None

    for row in rows:
        curr_cells_list = row.find_all("td")        
        
        if len(curr_cells_list) >= 8:
            coins_data.append(
                CoinData(
                    name = curr_cells_list[2].text,
                    price = curr_cells_list[3].text,
                    market_cap = curr_cells_list[7].text,
                    volume_24 = curr_cells_list[8].text
                )
            )

    for i, coin in enumerate(coins_data, start = 1):
        print(f'{i} -> {coin}')

#TODO:put this into a constants folder
ONE_MIN = 60

if __name__ == "__main__":
    #main()
    while True:     
        main()
        sleep(ONE_MIN * 5)
        
