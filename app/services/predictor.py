from app.utils.image_utils import read_image
from app.predictors.Yolov8Classifier import Yolov8Classifier
from app.predictors.ResNetClassifier import ResNetClassifier

model_map = {
    "yolov8-cls": Yolov8Classifier(),  
    "resnet": ResNetClassifier(),
}

TECHNO_MAP = {
    "zone agricole": "2G",
    "zone industrielle": "3G",
    "zone urbaine dense": "4G",
    "zone urbaine faible": "3G",
    "zone urbaine moderee": "4G",
    "zone vide": "2G"
}



async def predict_image(file, model_name: str):
    image = await read_image(file)
    model = model_map.get(model_name)
    if model is None:
        return "Modèle inconnu"

    final = model.predict(image)
    return final




async def predict_class(img, model_name: str):
    
    model = model_map.get(model_name)
    if model is None:
        return "Modèle inconnu"

    zone = model.predict(img)

    techno = TECHNO_MAP.get(zone, "2G")



    return {
        "zone_predite": zone,
        "antenne_suggeree": techno,
    }

    