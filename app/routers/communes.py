from fastapi import APIRouter
from app.entities.Commune import Commune
from app.entities.Wilaya import Wilaya
from app.database import database
from sqlalchemy import select, func
from fastapi import HTTPException

router = APIRouter(
    prefix="/communes",
    tags=["Communes"]
)

@router.get("/all")
async def get_communes():
    query = select(Commune)
    result = await database.fetch_all(query)
    return result

@router.get("/by_wilaya/{wilaya_id}")
async def get_communes_by_wilaya(wilaya_id: int):
    query = select(Commune).where(Commune.wilaya_id == wilaya_id)
    result = await database.fetch_all(query)
    
    if not result:
        raise HTTPException(status_code=404, detail="Communes not found for the given wilaya_id")
    
    return result




@router.get("/by_wilaya_name/{wilaya_name}")
async def get_communes_by_wilaya(wilaya_name: str):
    query = select(Commune).join(Commune.wilaya).where(Wilaya.name.ilike(f"{wilaya_name}%"))
    results = await database.fetch_all(query)

    return [
        {
            "commune_id": row["id"],
            "commune_name": row["name"],
            "latitude": row["latitude"],
            "longitude": row["longitude"],
            "wilaya_id": row["wilaya_id"]
        }
        for row in results
    ]








@router.get("/by_id/{id}")
async def get_commune(id: int):
    query = select(Commune).where(Commune.id == id)
    result = await database.fetch_one(query)
    
    if not result:
        raise HTTPException(status_code=404, detail="Commune not found")
    
    return result

@router.get("/by_name/{name}")
async def get_commune(name: str):
    query = select(Commune).where(Commune.name.ilike(f"%{name}%"))
    result = await database.fetch_all(query)
    
    if not result:
        raise HTTPException(status_code=404, detail="Commune not found")
    
    return result



@router.get("/communes_total")
async def get_total_communes():
    query = select(func.count()).select_from(Commune)
    total = await database.fetch_val(query)
    return {"total_communes": total}
