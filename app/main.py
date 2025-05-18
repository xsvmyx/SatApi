from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import database
from app.routers import predict,zones,wilayas,communes,detect,bts ,clients
from app.database import engine
from app.database import Base
# import logging


app = FastAPI()

@app.on_event("startup")
async def startup():
    print("🔧 Création des tables...")
    Base.metadata.create_all(bind=engine)
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
   
    await database.disconnect()



# Ajouter le middleware CORS pour autoriser les requêtes
origins = [
    "http://localhost",
    "http://127.0.0.1",
    "http://localhost:8000",  # Si ton API tourne sur 8000
]
#pour le mom on laisse les origines de coté
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],      # ✅ Toutes les origines (domaines) autorisées
    allow_credentials=False,  # ✅ Obligatoire pour utiliser "*" dans allow_origins
    allow_methods=["*"],      # ✅ Toutes les méthodes HTTP autorisées (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],      # ✅ Tous les headers autorisés
)


# logging.basicConfig(level=logging.DEBUG)
app.include_router(zones.router)
app.include_router(predict.router)
app.include_router(wilayas.router)
app.include_router(communes.router)
app.include_router(bts.router)
app.include_router(detect.router)
app.include_router(clients.router)


# logging.debug("Router bien inclus")