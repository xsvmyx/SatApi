from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import database
from app.routers import predict,zones
from app.database import engine
from app.database import Base

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

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Permet de spécifier les origines autorisées
    allow_credentials=True,
    allow_methods=["*"],  # Autoriser toutes les méthodes HTTP (GET, POST, etc.)
    allow_headers=["*"],  # Autoriser tous les headers
)

app.include_router(zones.router)
app.include_router(predict.router)
