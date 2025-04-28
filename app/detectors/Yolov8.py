from ultralytics import YOLO
import os

class Yolov8:
    def __init__(self):
        print("[INFO] Chargement du modèle YOLOv8")
        model_path = os.path.join(os.path.dirname(__file__), '../../models/Yolov8.pt')
        self.model = YOLO(model_path)

    
    def detect(self,img):
        return self.model(img)[0]
        