from datetime import datetime, MINYEAR
from db.engine import crypto_data_table, init_data_base
from sqlalchemy import select, insert

db = init_data_base()

if db == False:
    raise Exception("An error ocurred while trying to connect to the data base.")


#Este metodo retorna la fecha mas antigua de la moneda en cuestion, de lo contrario retorna ??? 
def get_min_date_for_coin(coin_name: str) -> datetime:
    with db.connect() as conn:
        res = conn.execute(select(crypto_data_table.c.scraped_at).where(
            crypto_data_table.c.coin_name == coin_name,
        ).order_by(
            crypto_data_table.c.scraped_at
            ).limit(1))
        
        res = list(res) 
        conn.close()
        
        if len(res) == 0:
            return datetime.now()#It makes sence, isnt it ?

        return res[0][0]


#Este metodo retorna el precio de la primera fecha in el intervalo:
# [star_date, now]
def get_price_from(coin_name: str, start_date: datetime) -> float | None:#This is like an option    
    with db.connect() as conn:
        res = conn.execute(
        select(
            crypto_data_table.c.price).where(
                crypto_data_table.c.coin_name == coin_name, 
                crypto_data_table.c.scraped_at >= start_date).limit(1))

        res = list(res)
        conn.close()
        return res[0][0] if len(res) == 1 else None


#Este metodo retorna el ultimo precio de la moneda que cumpla con la fecha dada:
def get_price_until(coin_name: str, end_date: datetime) -> float | None:
    with db.connect() as conn:
        res = conn.execute(
            #TODO:Buscar la menera de no tener que traer todas las tuplas antes de tomar el ultimo elemento.
            select(
                crypto_data_table.c.price).where(
                    crypto_data_table.c.coin_name == coin_name,
                    crypto_data_table.c.scraped_at <= end_date
                ).order_by(crypto_data_table.c.scraped_at)
            )
        
        res = list(res)
        conn.close()

        if len(res) == 0:
            return None

        return res[len(res) - 1][0]

def insert_coin_data(data):
    with db.connect() as conn:
        conn.execute(insert(crypto_data_table), data)            
        conn.commit()
        conn.close()

def compute_avg_in_interval(coin_name: str, start_date: datetime, end_date: datetime) -> float | None:
    with db.connect() as conn:
        res = conn.execute(
            select(crypto_data_table.c.price).where(
                crypto_data_table.c.coin_name == coin_name,
                crypto_data_table.c.scraped_at >= start_date,
                crypto_data_table.c.scraped_at <= end_date,
            )
        )
        
        res = list(res)
        conn.close()
        
        if len(res) == 0:
            return None

        return round(sum([tup[0] for tup in res]) / len(res), 3)


def compute_volue_market_cap_ratio(coin_name: str, start_date: datetime, end_date: datetime) -> float | None:
    with db.connect() as conn:
        res = conn.execute(
            select(crypto_data_table.c.volume_24, crypto_data_table.c.market_cap).where(
                crypto_data_table.c.coin_name == coin_name,
                crypto_data_table.c.scraped_at >= start_date,
                crypto_data_table.c.scraped_at <= end_date,
            )
        )

        res = list(res)
        conn.close()    
        
        if len(res) == 0:
            return None

        return sum([volume / market_cap for volume, market_cap in res]) / len(res)


def get_coin_data(coin_name: str, start_date: datetime, end_date: datetime) -> list[dict] | None:
    with db.connect() as conn:
        res = conn.execute(
            select(
                crypto_data_table.c.price,
                crypto_data_table.c.market_cap,
                crypto_data_table.c.volume_24).where(
                crypto_data_table.c.coin_name == coin_name,
                crypto_data_table.c.scraped_at >= start_date,
                crypto_data_table.c.scraped_at <= end_date,
            )
        )
    
        res = list(res)
        conn.close()    
        
        if len(res) == 0:
            return None
        
        return [{"price": p, "market_cap": mc, "volume_24": v} for p, mc, v in res]                
