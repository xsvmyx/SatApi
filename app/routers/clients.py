from fastapi import APIRouter
from app.entities.Client import Client
from app.entities.Bts import BTS
from app.entities.Commune import Commune
from app.entities.Wilaya import Wilaya
from app.entities.Zone import Zone
from app.database import database
from sqlalchemy import select , func
from fastapi import HTTPException

router = APIRouter(
    prefix="/clients",
    tags=["clients"]
)

@router.get("/all")
async def get_clients():
    query = select(Client)
    result = await database.fetch_all(query)
    return result



@router.get("/by_id/{id}")
async def get_client_by_id(id: int):
    query = select(Client).where(Client.client_id == id)
    result = await database.fetch_one(query)
    
    if not result:
        raise HTTPException(status_code=404, detail="client not found")
    
    return result


@router.get("/by_bts/{bts}")
async def get_clients_by_bts(bts : str):
    query = select(Client).where(Client.bts_code.ilike(f"%{bts}%"))
    result = await database.fetch_all(query)
    
    if not result:
        raise HTTPException(status_code=404, detail="Clients not found for the given 'bts code'")
    
    return result



@router.get("/clients_by_commune_id/{commune_id}")
async def get_clients_by_commune(commune_id: int):
    
    query_bts = select(BTS).where(BTS.commune_id == commune_id)
    bts_list = await database.fetch_all(query_bts)

    if not bts_list:
        raise HTTPException(status_code=404, detail="Aucun BTS trouvé pour cette commune.")

   
    bts_codes = [bts["code"] for bts in bts_list]

   
    query_clients = select(Client).where(Client.bts_code.in_(bts_codes))
    clients = await database.fetch_all(query_clients)

    if not clients:
        raise HTTPException(status_code=404, detail="Aucun client trouvé pour cette commune.")

    return clients




@router.get("/clients_par_commune")
async def get_clients_by_commune(commune_name: str, wilaya_id: int):
    
    query_commune = select(Commune).where(
        Commune.name.ilike(commune_name),
        Commune.wilaya_id == wilaya_id
    )
    commune = await database.fetch_one(query_commune)

    if not commune:
        raise HTTPException(status_code=404, detail="Commune non trouvée.")

    
    query_bts = select(BTS).where(BTS.commune_id == commune["id"])
    bts_list = await database.fetch_all(query_bts)

    if not bts_list:
        raise HTTPException(status_code=404, detail="Aucun BTS trouvé pour cette commune.")

    bts_codes = [bts["code"] for bts in bts_list]

    
    query_clients = select(Client).where(Client.bts_code.in_(bts_codes))
    clients = await database.fetch_all(query_clients)

    if not clients:
        raise HTTPException(status_code=404, detail="Aucun client trouvé pour cette commune.")

    return clients



@router.get("/clients_by_wilaya_id/{wilaya_id}")
async def get_clients_by_wilaya(wilaya_id: int):
    
    query_communes = select(Commune).where(Commune.wilaya_id == wilaya_id)
    communes = await database.fetch_all(query_communes)

    if not communes:
        raise HTTPException(status_code=404, detail="Aucune commune trouvée pour cette wilaya.")

    commune_ids = [commune["id"] for commune in communes]

    
    query_bts = select(BTS).where(BTS.commune_id.in_(commune_ids))
    bts_list = await database.fetch_all(query_bts)

    if not bts_list:
        raise HTTPException(status_code=404, detail="Aucun BTS trouvé pour cette wilaya.")

    bts_codes = [bts["code"] for bts in bts_list]

    
    query_clients = select(Client).where(Client.bts_code.in_(bts_codes))
    clients = await database.fetch_all(query_clients)

    if not clients:
        raise HTTPException(status_code=404, detail="Aucun client trouvé pour cette wilaya.")

    
    return clients




@router.get("infos_clients_by_wilaya_id/{wilaya_id}")
async def get_clients_by_wilaya(wilaya_id: int):
    
    query_communes = select(Commune).where(Commune.wilaya_id == wilaya_id)
    communes = await database.fetch_all(query_communes)

    if not communes:
        raise HTTPException(status_code=404, detail="Aucune commune trouvée pour cette wilaya.")

    commune_map = {commune["id"]: commune["name"] for commune in communes}

    
    commune_ids = list(commune_map.keys())
    query_bts = select(BTS).where(BTS.commune_id.in_(commune_ids))
    bts_list = await database.fetch_all(query_bts)

    if not bts_list:
        raise HTTPException(status_code=404, detail="Aucun BTS trouvé pour cette wilaya.")

    bts_code_to_commune_id = {bts["code"]: bts["commune_id"] for bts in bts_list}
    bts_codes = list(bts_code_to_commune_id.keys())

    
    query_clients = select(Client).where(Client.bts_code.in_(bts_codes))
    clients = await database.fetch_all(query_clients)

    if not clients:
        raise HTTPException(status_code=404, detail="Aucun client trouvé pour cette wilaya.")

    
    enriched_clients = []
    for client in clients:
        bts_code = client["bts_code"]
        commune_id = bts_code_to_commune_id.get(bts_code)
        commune_name = commune_map.get(commune_id)

        enriched_client = dict(client)
        enriched_client["commune_name"] = commune_name
        enriched_client["commune_id"] = commune_id
        enriched_client["wilaya_id"] = wilaya_id
        enriched_clients.append(enriched_client)

    return enriched_clients



@router.get("/clients_total")
async def get_total_clients():
    query = select(func.count()).select_from(Client)
    total = await database.fetch_val(query)
    return {"total_clients": total}




@router.get("/clients_total/par_zone/{zone_id}")
async def get_clients_count_by_zone(zone_id : int):
    query = (
    select(Zone.id, func.count(Client.client_id))
    .join(Zone.wilayas)
    .join(Wilaya.communes)
    .join(Commune.bts)
    .join(BTS.clients)
    .where(Zone.id == zone_id)
    .group_by(Zone.id)
)
    results = await database.fetch_one(query)
    return {"zone": results[0], "total_clients": results[1]}




@router.get("/clients_total/pour_chaque_zone")
async def get_clients_count_for_each_zone():
    query = (
        select(Zone.id, func.count(Client.client_id))
        .join(Zone.wilayas)
        .join(Wilaya.communes)
        .join(Commune.bts)
        .join(BTS.clients)
        .group_by(Zone.id)
    )
    results = await database.fetch_all(query)
    return [{"zone": row[0], "total_clients": row[1]} for row in results]




@router.get("/clients_total/par_wilaya/{wilaya_id}")
async def get_clients_count_by_wilaya(wilaya_id : int):
    query = (
        select(Wilaya.id, func.count(Client.client_id))
        .join(Wilaya.communes)
        .join(Commune.bts)
        .join(BTS.clients)
        .where(Wilaya.id == wilaya_id)
        .group_by(Wilaya.id)
    )
    results = await database.fetch_one(query)
    return {"wilaya": results[0], "total_clients": results[1]}



@router.get("/clients_total/pour_chaque_wilaya")
async def get_clients_count_for_each_wilaya():
    query = (
        select(Wilaya.id, func.count(Client.client_id))
        .join(Wilaya.communes)
        .join(Commune.bts)
        .join(BTS.clients)
        .group_by(Wilaya.id)
    )
    results = await database.fetch_all(query)
    return [{"wilaya": row[0], "total_clients": row[1]} for row in results]



@router.get("/clients_total/par_commune/{commune_id}")
async def get_clients_count_by_commune(commune_id : int):
    query = (
        select(Commune.id,Commune.name ,func.count(Client.client_id))
        .join(Commune.bts)
        .join(BTS.clients)
        .where(Commune.id == commune_id)
        .group_by(Commune.id)
    )
    results = await database.fetch_one(query)
    return {"commune": results[0],"total_clients": results[2],"nom commune":results[1]} 




@router.get("/clients_total/pour_chaque_commune")
async def get_clients_count_for_each_commune():
    query = (
        select(Commune.id,Commune.name , func.count(Client.client_id))
        .join(Commune.bts)
        .join(BTS.clients)
        .group_by(Commune.id)
    )
    results = await database.fetch_all(query)
    return [{"commune": row[0],"total_clients": row[2],"nom commune":row[1]}  for row in results]



@router.get("/clients_total/par_bts/{bts_code}")
async def get_clients_count_by_bts_code(bts_code: str):
    query = (
        select(BTS.code, func.count(Client.client_id))
        .join(Client)
        .where(BTS.code == bts_code)
        .group_by(BTS.code)
    )
    result = await database.fetch_one(query)

    if not result:
        return {"bts_code": bts_code, "total_clients": 0}

    return {"bts_code": result[0], "total_clients": result[1]}




@router.get("/clients_total/pour_chaque_bts")
async def get_clients_count_by_bts():
    query = (
    select(BTS.code, func.count(Client.client_id))
    .join(Client)
    .group_by(BTS.code)
)
    results = await database.fetch_all(query)

    return [{"bts_code": row[0], "total_clients": row[1]} for row in results]