from fastapi import APIRouter
from app.entities.Zone import Zone
from app.database import database
from sqlalchemy import select
from fastapi import HTTPException

router = APIRouter(
    prefix="/zones",
    tags=["Zones"]
)

@router.get("/all")
async def get_zones():
    query = select(Zone)
    result = await database.fetch_all(query)
    return result

@router.get("/by_id/{id}")
async def get_zone(id: int):
    query = select(Zone).where(Zone.id == id)
    result = await database.fetch_one(query)
    
    if not result:
        raise HTTPException(status_code=404, detail="Communes not found for the given wilaya_id")
    
    return result