from fastapi import APIRouter
from app.entities.Bts import BTS
from app.entities.Commune import Commune
from app.database import database
from sqlalchemy import select
from fastapi import HTTPException

router = APIRouter(
    prefix="/bts",
    tags=["BTS"]
)

@router.get("/all")
async def get_bts():
    query = select(BTS)
    result = await database.fetch_all(query)
    return result



@router.get("/by_code/{code}")
async def get_bts_by_code(code: str):
    query = select(BTS).where(BTS.code.ilike(f"%{code}%"))
    result = await database.fetch_all(query)
    
    if not result:
        raise HTTPException(status_code=404, detail="bts not found")
    
    return result


@router.get("/by_commune_id/{id}")
async def get_bts_by_commune_id(id: int):
    query = select(BTS).where(BTS.id == id)
    result = await database.fetch_all(query)
    
    if not result:
        raise HTTPException(status_code=404, detail="bts not found")
    
    return result


@router.get("/by_group/{group}")
async def get_bts_by_group(group: str):
    query = select(BTS).where(BTS.groupe.ilike(f"%{group}%"))
    result = await database.fetch_all(query)
    
    if not result:
        raise HTTPException(status_code=404, detail="bts not found")
    
    return result


@router.get("/bts_par_commune")
async def get_bts_by_commune(commune_name: str, wilaya_id: int):
    #recuperer la commune avec nom + wilaya
    query_commune = query_commune = query_commune = select(Commune).where(
    Commune.name.ilike(commune_name), Commune.wilaya_id == wilaya_id
)
    commune = await database.fetch_one(query_commune)

    if not commune:
        raise HTTPException(status_code=404, detail="bts non trouvée.")

    #bts liés à cette commune
    query_bts = select(BTS).where(BTS.commune_id == commune["id"])
    bts_list = await database.fetch_all(query_bts)

    return bts_list




