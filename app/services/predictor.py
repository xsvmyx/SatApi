from app.utils.image_utils import read_image
from app.models.Yolov8Classifier import Yolov8Classifier
from app.models.ResNetClassifier import ResNetClassifier

model_map = {
    "yolov8-cls": Yolov8Classifier(),  
    #"resnet": ResNetClassifier(),
}




async def predict_image(file, model_name: str):
    image = await read_image(file)
    model = model_map.get(model_name)
    if model is None:
        return "Modèle inconnu"

    

    final = model.predict(image)
    return final



