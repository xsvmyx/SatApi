from fastapi import APIRouter
from fastapi.responses import JSONResponse
from app.services.detector import detect_image
from app.utils.PredictRequest import PredictRequest

router = APIRouter()

@router.post("/detect")
async def detect(payload: PredictRequest):
    
    try:
        
        result = await detect_image(payload)
        return result
    except Exception as e:
        return JSONResponse(status_code=500, content={"error dans /detect !!": str(e)})



