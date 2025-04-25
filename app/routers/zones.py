from fastapi import APIRouter
from app.entities.Zone import Zone
from app.database import database
from sqlalchemy import select

router = APIRouter()

@router.get("/zones")
async def get_zones():
    query = select(Zone)
    result = await database.fetch_all(query)
    return result

