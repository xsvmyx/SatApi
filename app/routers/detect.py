from fastapi import APIRouter,HTTPException
from fastapi.responses import JSONResponse
from app.services.detector import detect_image
from app.utils.PredictRequest import PredictRequest
from app.utils.image_utils import decode_image
import os
from ultralytics import YOLO


router = APIRouter()

# @router.post("/detect")
# async def detect(payload: PredictRequest):
    
#     try:
        
#         result = await detect_image(payload)
#         return result
#     except Exception as e:
#         return JSONResponse(status_code=500, content={"error dans /detect !!": str(e)})




model_path = os.path.join(os.path.dirname(__file__), '../../models/Yolov8.pt')
model = YOLO(model_path)



@router.post("/detect")
async def predict(payload: PredictRequest):
    
    try:
        img = decode_image(payload.image)
    except Exception:
        raise HTTPException(status_code=400, detail="Image invalide")
    

    w, h = img.size

    # bornes géographiques
    lat_top = payload.latTop
    lat_bottom = payload.latBottom
    lon_left = payload.lonLeft
    lon_right = payload.lonRight

    # prédiction
    results = model(img)[0]

    boxes = []
    for box in results.boxes:
        x1, y1, x2, y2 = box.xyxy[0].tolist()
        cls_id = int(box.cls[0])

        # conversion pixel->latlon
        lat1 = lat_top    + (y1 / h) * (lat_bottom - lat_top)
        lon1 = lon_left   + (x1 / w) * (lon_right  - lon_left)
        lat2 = lat_top    + (y2 / h) * (lat_bottom - lat_top)
        lon2 = lon_left   + (x2 / w) * (lon_right  - lon_left)

        boxes.append({
            "lat1": lat1, "lon1": lon1,
            "lat2": lat2, "lon2": lon2,
            "class": cls_id
        })



    return JSONResponse(content={"bboxes": boxes})




