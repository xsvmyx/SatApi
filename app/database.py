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
# import random
# import numpy as np


# db = SessionLocal()

# Liste pondérée (plus de "3g")
#GEN_VALUES = ['2g','2g','2g','3g', '3g', '3g', '3g', '3g','4g' ,'4g' ,'4g', '5g']
# bts_list = db.query(BTS).filter(BTS.gen != None).all()
# for bts in bts_list:
#     bts.gen = random.choice(GEN_VALUES)



# RADIUS_VALUES = [1,1,1,2,2,2,2,3,3,4]
# bts_list = db.query(BTS).filter(BTS.radius == None).all()
# for bts in bts_list:
#     bts.radius = random.choice(RADIUS_VALUES)






# # Paramètres de la distribution
# # Tranches d'âge et leur poids (approximatif en %)
# age_bins = [
#     (18, 24),  # ~25%
#     (25, 34),  # ~25%
#     (35, 44),  # ~20%
#     (45, 54),  # ~15%
#     (55, 64),  # ~10%
#     (65, 74),  # ~4%
#     (75, 90),  # ~1%
# ]
# weights = [25, 25, 20, 15, 10, 4, 1]
# weights = np.array(weights) / np.sum(weights)  # Normalize to sum to 1

# # Fonction pour tirer un âge aléatoire selon les poids
# def generate_random_age():
#     selected_bin = age_bins[np.random.choice(len(age_bins), p=weights)]
#     return np.random.randint(selected_bin[0], selected_bin[1] + 1)

# # Mettre à jour les clients
# clients = db.query(Client).all()
# for client in clients:
#     client.age = generate_random_age()








#db.query(Client).delete()

#db.add_all(clients)

# db.commit()
# db.close()

# print(" avec succès")     
