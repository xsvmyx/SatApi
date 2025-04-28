from ultralytics import YOLO
import os

class Yolov8Classifier:
    def __init__(self):
        print("[INFO] Chargement du modèle YOLOv8-CLS")
        model_path = os.path.join(os.path.dirname(__file__), '../../models/yolov8_cls_best.pt')
        self.model = YOLO(model_path)
      
        


    def predict(self, image_bytes) :
        
        results = self.model(image_bytes)
        
        #confidence = float(results[0].probs.top1conf)

        print(f"\nClasse prédite: ")
    
        top_class = results[0].probs.top1 
        
        print(f"\nClasse prédite: ")
        match top_class:
            case 0:
                prediction = "Zone agricole"
            case 1:
                prediction = "Zone industrielle"
            case 2:
                prediction = "Zone urbaine dense"
            case 3:
                prediction = "Zone urbaine faible"
            case 4:
                prediction = "zone urbaine modérée"
            case 5:
                prediction = "Zone vide"

        return prediction
































# from ultralytics import YOLO
# import os

# def load_model():
#     model_path = os.path.join(os.path.dirname(__file__), '../../models/yolov8_cls_best.pt')
#     model = YOLO(model_path)
#     return model

# def predict(model,final):
#     results = model(final)
    
#     print(f"\nClasse prédite: ")
    
#     top_class = results[0].probs.top1 
       
#     print(f"\nClasse prédite: ")
#     match top_class:
#         case 0:
#             prediction = "Zone agricole"
#         case 1:
#             prediction = "Zone industrielle"
#         case 2:
#             prediction = "Zone urbaine dense"
#         case 3:
#             prediction = "Zone urbaine faible"
#         case 4:
#             prediction = "Zone urbaine moderee"
#         case 5:
#             prediction = "Zone vide"

#     return prediction