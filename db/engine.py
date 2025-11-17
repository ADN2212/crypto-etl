from sqlalchemy import create_engine,  MetaData, Table, Column, Integer, String, DateTime, Double, Engine
from dotenv import load_dotenv 
from os import getenv


load_dotenv()

metadata = MetaData()

crypto_data_table = Table(
            'crypto_data',
            metadata,
            Column('id', Integer, primary_key = True),
            Column('coin_name', String),
            Column('price', Double),
            Column('market_cap', Double),
            Column('volume_24', Double),
            Column('scraped_at', DateTime)   
    )


DATA_BASE_URL = getenv("DATA_BASE_URL")

def init_data_base() -> Engine | bool:
    
    try:
        engine = create_engine(DATA_BASE_URL)
    except BaseException as err:
        print(f'An error occurred while initializing the database => "{err}"')
        return False

    try:
        metadata.create_all(engine)
    except BaseException  as err:
        print(f'An error occurred while initializing the database => "{err}"')
        return False
    
    
    print("data base intialized succesfully")
    return engine
