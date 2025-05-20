from fastapi import APIRouter, UploadFile, File, Form
from fastapi.responses import JSONResponse
from app.services.predictor import predict_image,predict_class
from app.utils.Request import BTSpred
from app.database import database
from sqlalchemy import select 
from app.entities.Bts import BTS
from app.utils.image_utils import  build_maptiler_url,download_maptiler_image,build_mapbox_url,download_mapbox_image
from fastapi import HTTPException
from app.utils.Tokens import MAPBOX_API_KEY,MAPTILER_API_KEY


router = APIRouter()

@router.post("/predict")
async def predict(file: UploadFile = File(...), model_name: str = Form(...)):
    try:
        result = await predict_image(file, model_name)
        return result
    except Exception as e:
        return JSONResponse(status_code=501, content={"error!!": str(e)})
    




@router.post("/predict_gen")
async def predict_gen(payload: BTSpred):

    query = select(BTS).where(BTS.code.ilike(f"{payload.code}%"))
    bts = await database.fetch_one(query)
    if not bts:
        raise HTTPException(status_code=404, detail="bts not found")


    lat = bts["latitude"]
    lon = bts["longitude"]
    radius = bts["radius"]
    #token = MAPTILER_API_KEY  #token pour maptiler
    #url = build_maptiler_url(lat,lon,radius,token)

    token = MAPBOX_API_KEY  #token pour mapbox
    url = build_mapbox_url(lat, lon, radius, token)
    img_np = download_mapbox_image(url)
    
    try:
        result = await predict_class(img_np,payload.model)
        return result
    except Exception as e:
        return JSONResponse(status_code=501, content={"error dans la predict_class": str(e)})




