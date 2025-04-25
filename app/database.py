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




# from app.entities.Zone import Zone
# from app.entities.Wilaya import Wilaya
# from app.entities.Commune import Commune


# zones = [
#     Zone(name="zone1", latitude="35.107911", longitude="2.874479"),
#     Zone(name="zone2", latitude="34.643428", longitude="-0.022995"),
#     Zone(name="zone3", latitude="35.434197", longitude="6.304822"),
#     Zone(name="zone4", latitude="32.270941", longitude="3.237608"),
#     Zone(name="zone5", latitude="26.332856", longitude="1.744284")
# ]



# wilayas = [
#     Wilaya(id=1, name="Adrar", latitude="27.8743", longitude="-0.2939", zone_id=1),  # Sud
#     Wilaya(id=2, name="Chlef", latitude="36.1653", longitude="1.3340", zone_id=3),  # Nord-Centre
#     Wilaya(id=3, name="Laghouat", latitude="33.8006", longitude="2.8809", zone_id=2),  # Hauts Plateaux
#     Wilaya(id=4, name="Oum El Bouaghi", latitude="35.8754", longitude="7.1135", zone_id=4),  # Nord-Est
#     Wilaya(id=5, name="Batna", latitude="35.5556", longitude="6.1744", zone_id=4),  # Nord-Est
#     Wilaya(id=6, name="Béjaïa", latitude="36.7519", longitude="5.0550", zone_id=4),  # Nord-Est
#     Wilaya(id=7, name="Biskra", latitude="34.8504", longitude="5.7280", zone_id=2),  # Hauts Plateaux
#     Wilaya(id=8, name="Béchar", latitude="31.6187", longitude="-2.2140", zone_id=1),  # Sud
#     Wilaya(id=9, name="Blida", latitude="36.4700", longitude="2.8277", zone_id=3),  # Nord-Centre
#     Wilaya(id=10, name="Bouira", latitude="36.3769", longitude="3.9020", zone_id=3),  # Nord-Centre
#     Wilaya(id=11, name="Tamanrasset", latitude="22.7850", longitude="5.5228", zone_id=1),  # Sud
#     Wilaya(id=12, name="Tébessa", latitude="35.4042", longitude="8.1240", zone_id=4),  # Nord-Est
#     Wilaya(id=13, name="Tlemcen", latitude="34.8828", longitude="-1.3160", zone_id=3),  # Nord-Centre
#     Wilaya(id=14, name="Tiaret", latitude="35.3713", longitude="1.3160", zone_id=2),  # Hauts Plateaux
#     Wilaya(id=15, name="Tizi Ouzou", latitude="36.7133", longitude="4.0459", zone_id=3),  # Nord-Centre
#     Wilaya(id=16, name="Alger", latitude="36.7538", longitude="3.0588", zone_id=3),  # Nord-Centre
#     Wilaya(id=17, name="Djelfa", latitude="34.6704", longitude="3.2504", zone_id=2),  # Hauts Plateaux
#     Wilaya(id=18, name="Jijel", latitude="36.8206", longitude="5.7660", zone_id=4),  # Nord-Est
#     Wilaya(id=19, name="Sétif", latitude="36.1911", longitude="5.4137", zone_id=4),  # Nord-Est
#     Wilaya(id=20, name="Saïda", latitude="34.8303", longitude="0.1517", zone_id=2),  # Hauts Plateaux
# ]

# communes = [
#     Commune(name="Bab El Oued", latitude=36.7989, longitude=3.0588, wilaya_id=16),
#     Commune(name="El Madania", latitude=36.7486, longitude=3.0714, wilaya_id=16),
#     Commune(name="El Harrach", latitude=36.7157, longitude=3.1202, wilaya_id=16),
#     Commune(name="Hussein Dey", latitude=36.7457, longitude=3.0861, wilaya_id=16),
#     Commune(name="Kouba", latitude=36.7296, longitude=3.0863, wilaya_id=16),
#     Commune(name="Bir Mourad Raïs", latitude=36.7354, longitude=3.0463, wilaya_id=16),
#     Commune(name="Birkhadem", latitude=36.7011, longitude=3.0307, wilaya_id=16),
#     Commune(name="El Magharia", latitude=36.7481, longitude=3.0763, wilaya_id=16),
#     Commune(name="Belouizdad", latitude=36.7532, longitude=3.0739, wilaya_id=16),
#     Commune(name="Casbah", latitude=36.7836, longitude=3.0586, wilaya_id=16),
#     Commune(name="Oued Koriche", latitude=36.7821, longitude=3.0389, wilaya_id=16),
#     Commune(name="Bologhine", latitude=36.8105, longitude=3.0313, wilaya_id=16),
#     Commune(name="Bir Mourad Raïs", latitude=36.7330, longitude=3.0510, wilaya_id=16),
#     Commune(name="Bordj El Kiffan", latitude=36.7590, longitude=3.1975, wilaya_id=16),
#     Commune(name="Dar El Beïda", latitude=36.7152, longitude=3.2194, wilaya_id=16),
#     Commune(name="Bab Ezzouar", latitude=36.7169, longitude=3.1851, wilaya_id=16),
#     Commune(name="Draria", latitude=36.6983, longitude=2.9952, wilaya_id=16),
#     Commune(name="Ouled Fayet", latitude=36.7193, longitude=2.9514, wilaya_id=16),
#     Commune(name="El Achour", latitude=36.7122, longitude=2.9826, wilaya_id=16)
# ]




# db = SessionLocal()




# #db.query(Commune).delete()
# db.add_all(communes)

# db.commit()
# db.close()

# print("Communes ajoutées avec succès")        