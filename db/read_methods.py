from datetime import datetime
from db.engine import crypto_data_table, init_data_base
from sqlalchemy import select

db = init_data_base()

if db == False:
    raise Exception("An error ocurred while trying to connect to the data base.")

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
#Es decir, si la fecha es 2025-11-15, este metodo reotornara el ultimo precio en el intertvalo:
# [2025-11-15-0-0-0, 2025-11-15-23-59-59]
def get_price_until(coin_name: str, end_date: datetime) -> float | None:
    with db.connect() as conn:
        res = conn.execute(
            select(
                crypto_data_table.c.price).where(
                    crypto_data_table.c.coin_name == coin_name,
                    crypto_data_table.c.scraped_at <= datetime(
                        year=end_date.year,
                        month=end_date.month,
                        day=end_date.day,
                        hour=23,
                        minute=59,
                        second=59
                    ),
                )
            )

        res = list(res)
        conn.close()

        if len(res) == 0:
            return None

        #Get the las element, asumiendo que estan ordenadas en forma cronologica:
        return res[len(res) - 1][0]
