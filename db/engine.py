from sqlalchemy import create_engine,  MetaData, Table, Column, Integer, String, DateTime, Double

#TODO:these must be envars
DATA_BASE_URL='postgresql://postgres:123456@localhost:5432/crypto_prices'

# create a metadata object
metadata = MetaData()#What the hell is this ???

#Create the table
#Este objeto servira como referencia para hacer la querys con el ORM:
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

def init_data_base():
    
    try:
        engine = create_engine(DATA_BASE_URL)
    except:
        return False
    
    #Esto agrega el schema a la base de datos:
    metadata.create_all(engine)
    print("data base intialized succesfully")
    return engine #Cada llamada a esta funcion creara una instancia de la Base de Datos, es esto correcto ? o mejor usar un singleton ?

