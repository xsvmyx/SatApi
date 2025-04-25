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




from app.entities.Zone import Zone
from app.entities.Wilaya import Wilaya






# db = SessionLocal()


# zones = [
#     Zone(name="zone1", latitude="35.107911", longitude="2.874479"),
#     Zone(name="zone2", latitude="34.643428", longitude="-0.022995"),
#     Zone(name="zone3", latitude="35.434197", longitude="6.304822"),
#     Zone(name="zone4", latitude="32.270941", longitude="3.237608"),
#     Zone(name="zone5", latitude="26.332856", longitude="1.744284")
# ]

# # Ajoute les zones à la session
# db.add_all(zones)

# # Commit les changements dans la base de données
# db.commit()

# # Ferme la session
# db.close()

# print("Zones ajoutées avec succès")        