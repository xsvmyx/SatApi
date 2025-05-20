from fastapi import APIRouter
from app.entities.Bts import BTS
from app.entities.Commune import Commune
from app.entities.Wilaya import Wilaya
from app.entities.Zone import Zone
from app.database import database
from sqlalchemy import select , func
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
    query = select(BTS).where(BTS.code.ilike(f"{code}%"))
    result = await database.fetch_all(query)
    
    if not result:
        raise HTTPException(status_code=404, detail="bts not found")
    
    return result



@router.get("/bts_infos_by_code/{code}")
async def get_bts_by_code(code: str):
    query_bts = select(BTS).where(BTS.code.ilike(f"{code}%"))
    bts_list = await database.fetch_all(query_bts)

    if not bts_list:
        raise HTTPException(status_code=404, detail="BTS not found")

    results = []
    for bts in bts_list:
        commune_id = bts["commune_id"]

        query_commune = select(Commune).where(Commune.id == commune_id)
        commune = await database.fetch_one(query_commune)

        if not commune:
            continue  # ou skip, ou gérer autrement

        results.append({
            "bts_code": bts["code"],
            "latitude": bts["latitude"],
            "longitude": bts["longitude"],
            "gen": bts["gen"],
            "radius" : bts["radius"],
            "commune_name": commune["name"],
            "commune_id": bts["commune_id"],
            "wilaya_id": commune["wilaya_id"]
        })

    if not results:
        raise HTTPException(status_code=404, detail="No BTS with valid commune found")

    return results



@router.get("/by_commune_id/{id}")
async def get_bts_by_commune_id(id: int):
    query = select(BTS).where(BTS.commune_id == id)
    result = await database.fetch_all(query)
    
    if not result:
        raise HTTPException(status_code=404, detail="bts not found")
    
    return result




@router.get("/bts_par_commune")
async def get_bts_by_commune(commune_name: str, wilaya_id: int):
    #recuperer la commune avec nom + wilaya
    query_commune = select(Commune).where(
    Commune.name.ilike(commune_name), Commune.wilaya_id == wilaya_id
)
    commune = await database.fetch_one(query_commune)

    if not commune:
        raise HTTPException(status_code=404, detail="commune non trouvée.")

    #bts liés à cette commune
    query_bts = select(BTS).where(BTS.commune_id == commune["id"])
    bts_list = await database.fetch_all(query_bts)

    return bts_list




@router.get("/bts_par_wilaya/{wilaya_id}")
async def get_bts_par_wilaya(wilaya_id: int):
    
    query_communes = select(Commune).where(Commune.wilaya_id == wilaya_id)
    communes = await database.fetch_all(query_communes)

    if not communes:
        raise HTTPException(status_code=404, detail="Aucune commune trouvée pour cette wilaya.")

    
    commune_ids = [commune["id"] for commune in communes]

    
    query_bts = select(BTS).where(BTS.commune_id.in_(commune_ids))
    bts_list = await database.fetch_all(query_bts)

    if not bts_list:
        raise HTTPException(status_code=404, detail="Aucun BTS trouvé dans cette wilaya.")

    return bts_list




@router.get("/infos_bts_par_wilaya/{wilaya_id}")
async def get_bts_details_par_wilaya(wilaya_id: int):
    
    query_communes = select(Commune).where(Commune.wilaya_id == wilaya_id)
    communes = await database.fetch_all(query_communes)

    if not communes:
        raise HTTPException(status_code=404, detail="Aucune commune trouvée pour cette wilaya.")

    
    commune_map = {commune["id"]: commune["name"] for commune in communes}
    commune_ids = list(commune_map.keys())

    
    query_bts = select(BTS).where(BTS.commune_id.in_(commune_ids))
    bts_list = await database.fetch_all(query_bts)

    if not bts_list:
        raise HTTPException(status_code=404, detail="Aucun BTS trouvé dans cette wilaya.")

    
    bts_détails = []
    for bts in bts_list:
        commune_id = bts["commune_id"]
        nom_commune = commune_map.get(commune_id, "Inconnue")
        bts_détails.append({
            "code": bts["code"],
            "latitude": bts["latitude"],
            "longitude": bts["longitude"],
            "gen": bts["gen"],
            "radius" : bts["radius"],
            "commune": nom_commune,
            "commune_id": bts["commune_id"],
            "wilaya_id": wilaya_id
        })

    return bts_détails




@router.get("/bts_par_wilaya_name/{wilaya_name}")
async def get_bts_par_wilaya(wilaya_name: str):
    
    query_wilaya = select(Wilaya).where(Wilaya.name.ilike(wilaya_name))
    wilaya = await database.fetch_one(query_wilaya)

    if not wilaya:
        raise HTTPException(status_code=404, detail="Wilaya non trouvée.")

   
    query_communes = select(Commune).where(Commune.wilaya_id == wilaya["id"])
    communes = await database.fetch_all(query_communes)

    if not communes:
        raise HTTPException(status_code=404, detail="Aucune commune trouvée pour cette wilaya.")

    commune_ids = [commune["id"] for commune in communes]

    
    query_bts = select(BTS).where(BTS.commune_id.in_(commune_ids))
    bts_list = await database.fetch_all(query_bts)

    if not bts_list:
        raise HTTPException(status_code=404, detail="Aucun BTS trouvé dans cette wilaya.")

    return bts_list





@router.get("/infos_bts_par_wilaya_name/{wilaya_name}")
async def get_bts_details_par_wilaya(wilaya_name: str):
    
    query_wilaya = select(Wilaya).where(Wilaya.name.ilike(wilaya_name))
    wilaya = await database.fetch_one(query_wilaya)

    if not wilaya:
        raise HTTPException(status_code=404, detail="Wilaya non trouvée.")

    
    query_communes = select(Commune).where(Commune.wilaya_id == wilaya["id"])
    communes = await database.fetch_all(query_communes)

    if not communes:
        raise HTTPException(status_code=404, detail="Aucune commune trouvée pour cette wilaya.")

    commune_map = {commune["id"]: commune["name"] for commune in communes}
    commune_ids = list(commune_map.keys())

    
    query_bts = select(BTS).where(BTS.commune_id.in_(commune_ids))
    bts_list = await database.fetch_all(query_bts)

    if not bts_list:
        raise HTTPException(status_code=404, detail="Aucun BTS trouvé dans cette wilaya.")

    
    bts_détails = []
    for bts in bts_list:
        commune_id = bts["commune_id"]
        nom_commune = commune_map.get(commune_id, "Inconnue")
        bts_détails.append({
            "code": bts["code"],
            "latitude": bts["latitude"],
            "longitude": bts["longitude"],
            "gen": bts["gen"],
            "radius": bts["radius"],
            "commune": nom_commune,
            "commune_id": bts["commune_id"],
            "wilaya_id": wilaya["id"]
        })

    return bts_détails



@router.get("/bts_par_zone/{zone_id}")
async def get_bts_par_zone(zone_id: int):
    # 1. récupérer toutes les wilayas de la zone
    query_wilayas = select(Wilaya.id).where(Wilaya.zone_id == zone_id)
    wilayas = await database.fetch_all(query_wilayas)
    if not wilayas:
        raise HTTPException(status_code=404, detail="Aucune wilaya trouvée pour cette zone.")
    
    wilaya_ids = [w["id"] for w in wilayas]

    # 2. récupérer toutes les communes de ces wilayas
    query_communes = select(Commune.id).where(Commune.wilaya_id.in_(wilaya_ids))
    communes = await database.fetch_all(query_communes)
    if not communes:
        raise HTTPException(status_code=404, detail="Aucune commune trouvée dans ces wilayas.")

    commune_ids = [c["id"] for c in communes]

    # 3. récupérer tous les BTS dans ces communes
    query_bts = select(BTS).where(BTS.commune_id.in_(commune_ids))
    bts_list = await database.fetch_all(query_bts)
    if not bts_list:
        raise HTTPException(status_code=404, detail="Aucun BTS trouvé dans cette zone.")

    return bts_list







@router.get("/bts_total")
async def get_total_bts():
    query = select(func.count()).select_from(BTS)
    total = await database.fetch_val(query)
    return {"total_bts": total}



@router.get("/bts_total/par_zone/{zone_id}")
async def get_bts_count_by_zone(zone_id : int):
    query = (
    select(Zone.id, func.count(BTS.code))
    .join(Zone.wilayas)
    .join(Wilaya.communes)
    .join(Commune.bts)
    .where(Zone.id == zone_id)
    .group_by(Zone.id)
)
    results = await database.fetch_one(query)
    return {"zone": results[0], "total_bts": results[1]} 



@router.get("/bts_total/pour_chaque_zone")
async def get_bts_count_for_each_zone():
    query = (
        select(Zone.id, func.count(BTS.code))
        .join(Zone.wilayas)
        .join(Wilaya.communes)
        .join(Commune.bts)
        .group_by(Zone.id)
    )
    results = await database.fetch_all(query)
    return [{"zone": row[0], "total_bts": row[1]} for row in results]




@router.get("/bts_total/par_wilaya/{wilaya_id}")
async def get_bts_count_by_wilaya(wilaya_id : int):
    query = (
        select(Wilaya.id, func.count(BTS.code))
        .join(Wilaya.communes)
        .join(Commune.bts)
        .where(Wilaya.id == wilaya_id)
        .group_by(Wilaya.id)
    )
    results = await database.fetch_one(query)
    return {"wilaya": results[0], "total_bts": results[1]} 




@router.get("/bts_total/pour_chaque_wilaya")
async def get_bts_count_for_each_wilaya():
    query = (
        select(Wilaya.id, func.count(BTS.code))
        .join(Wilaya.communes)
        .join(Commune.bts)
        .group_by(Wilaya.id)
    )
    results = await database.fetch_all(query)
    return [{"wilaya": row[0], "total_bts": row[1]} for row in results]


 

@router.get("/bts_total/par_commune/{commune_id}")
async def get_bts_count_by_commune(commune_id : int):
    query = (
        select(Commune.id,Commune.name ,func.count(BTS.code))
        .join(Commune.bts)
        .where(Commune.id == commune_id)
        .group_by(Commune.id)
    )
    results = await database.fetch_one(query)
    return {"commune": results[0],"total_bts": results[2],"nom commune":results[1]} 



@router.get("/bts_total/pour_chaque_commune")
async def get_bts_count_for_each_commune():
    query = (
        select(Commune.id,Commune.name , func.count(BTS.code))
        .join(Commune.bts)
        .group_by(Commune.id)
    )
    results = await database.fetch_all(query)
    return [{"commune": row[0],"total_bts": row[2],"nom commune":row[1]}  for row in results]