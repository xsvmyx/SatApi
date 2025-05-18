from fastapi import APIRouter
from app.entities.Wilaya import Wilaya
from app.database import database
from sqlalchemy import select, func
from fastapi import HTTPException

router = APIRouter(
    prefix="/wilayas",
    tags=["Wilayas"]
)

@router.get("/all")
async def get_wilayas():
    query = select(Wilaya)
    result = await database.fetch_all(query)
    return result



@router.get("/by_zone/{zone_id}")
async def get_wilayas_by_zone(zone_id: int):
    query = select(Wilaya).where(Wilaya.zone_id == zone_id)
    result = await database.fetch_all(query)
    
    if not result:
        raise HTTPException(status_code=404, detail="Wilayas not found for the given zone_id")
    
    return result


@router.get("/by_id/{id}")
async def get_wilaya(id: int):
    query = select(Wilaya).where(Wilaya.id == id)
    result = await database.fetch_one(query)
    
    if not result:
        raise HTTPException(status_code=404, detail="Wilayas not found for the given id")
    
    return result


@router.get("/by_name/{name}")
async def get_wilaya(name: str):
    query = select(Wilaya).where(Wilaya.name.ilike(f"%{name}%"))
    result = await database.fetch_one(query)
    
    if not result:
        raise HTTPException(status_code=404, detail="Wilayas not found for the given name")
    
    return result


@router.get("/wilayas_total")
async def get_total_wilayas():
    query = select(func.count()).select_from(Wilaya)
    total = await database.fetch_val(query)
    return {"total_wilayas": total}