from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from databases import Database
import os


DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://postgres:postgres@localhost:5432/geo_data")


engine = create_engine(DATABASE_URL.replace("asyncpg", "psycopg2"))


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


Base = declarative_base()

# Connexion avec asyncpg pour les opérations asynchrones
database = Database(DATABASE_URL)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


###########################################################partie pour inserer 

# from app.entities.Zone import Zone
# from app.entities.Wilaya import Wilaya
# from app.entities.Commune import Commune
# from app.entities.Bts import BTS
# from app.entities.Client import Client
# import csv



# db = SessionLocal()



# #db.query(Client).delete()

# #db.add_all(clients)

# db.commit()
# db.close()

# print(" avec succès")        
