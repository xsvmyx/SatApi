from fastapi import APIRouter, UploadFile, File, Form
from fastapi.responses import JSONResponse
from app.services.predictor import predict_image

router = APIRouter()

@router.post("/predict")
async def predict(file: UploadFile = File(...), model_name: str = Form(...)):
    try:
        result = await predict_image(file, model_name)
        return result
    except Exception as e:
        return JSONResponse(status_code=501, content={"error!!": str(e)})