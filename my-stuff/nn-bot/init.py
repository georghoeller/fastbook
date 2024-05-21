from sqlalchemy import create_engine
#engine = create_engine("sqlite+pysqlite:///:memory:", echo=True)
# create database before 
engine = create_engine('sqlite:///BTCUSDTstream.db')
