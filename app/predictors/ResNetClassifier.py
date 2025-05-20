import torch
from torchvision import models, transforms
from PIL import Image
import numpy as np
import os
from torchvision.models import ResNet50_Weights

class ResNetClassifier:
    def __init__(self):
        print("[INFO] Chargement du modèle ResNet")
        model_path = os.path.join(os.path.dirname(__file__), '../../models/Resnet.pth')
        
        self.model = models.resnet50(weights=ResNet50_Weights.DEFAULT)
        self.model.fc = torch.nn.Linear(self.model.fc.in_features, 6)  # 6 classes
        self.model.load_state_dict(torch.load(model_path, map_location=torch.device('cpu')))
        self.model.eval()

        self.class_labels = [
            "zone agricole",
            "zone industrielle",
            "zone urbaine dense",
            "zone urbaine faible",
            "zone urbaine moderee",
            "zone vide"
        ]

        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model.to(self.device)

        self.preprocess = transforms.Compose([
            transforms.ToPILImage(),  # car tu reçois un numpy array
            transforms.Resize(256),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            transforms.Normalize(
                mean=[0.485, 0.456, 0.406],
                std=[0.229, 0.224, 0.225]
            )
        ])

    def predict(self, image_np):
        
        input_tensor = self.preprocess(image_np)
        input_batch = input_tensor.unsqueeze(0).to(self.device)

        with torch.no_grad():
            output = self.model(input_batch)
            probabilities = torch.nn.functional.softmax(output[0], dim=0)

        top_prob, top_class = torch.max(probabilities, 0)
        prediction = self.class_labels[top_class.item()]
        
        # print(f"Prédiction : {prediction} avec {top_prob.item()*100:.2f}%")
        print(f"Prédiction : {prediction} ")
        return prediction