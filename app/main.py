from fastapi import FastAPI, UploadFile, File, Form 
from app.services.predictor import predict_image
from app.services.TileLocation import get_coordinates_from_filename
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
app = FastAPI()

# Ajouter le middleware CORS pour autoriser les requêtes
origins = [
    "http://localhost",
    "http://127.0.0.1",
    "http://localhost:8000",  # Si ton API tourne sur 8000
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Permet de spécifier les origines autorisées
    allow_credentials=True,
    allow_methods=["*"],  # Autoriser toutes les méthodes HTTP (GET, POST, etc.)
    allow_headers=["*"],  # Autoriser tous les headers
)



@app.post("/predict")
async def predict(file: UploadFile = File(...), model_name: str = Form(...)):
    try:
      
        result = await predict_image(file,model_name)
       
        return result
    except Exception as e:
        return JSONResponse(status_code=501, content={"error!!": str(e)})

@app.post("/location")
async def locate(file: UploadFile = File(...)):
    return get_coordinates_from_filename(file.filename)


@app.post("/analyze")
async def analyze(file: UploadFile = File(...), model_name: str = Form(...)):
    try:
        
        prediction = await predict_image(file, model_name)

       
        lat , lon = get_coordinates_from_filename(file.filename)

        
        return {
            "filename": file.filename,
            "class": prediction,
            "latitude": lat,
            "longitude": lon
        }

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})



@app.get("/")
def root():
    return {"message": "Bienvenue sur SatAPI likip"}



# @app.post("/predict")
# async def predict(file: UploadFile = File(...), model_name: str = Form(...)):
#     prediction = await predict_image(file, model_name)
#     return {"prediction": prediction}
