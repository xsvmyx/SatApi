import io
import numpy as np
from PIL import Image
from fastapi import UploadFile

async def read_image(uploaded_file: UploadFile) -> np.ndarray:
    try:
        contents = await uploaded_file.read()
        image = Image.open(io.BytesIO(contents)).convert("RGB")
        image_np = np.array(image)
        return image_np
    except Exception as e:
        raise ValueError(f"Erreur lors de la lecture de l'image : {e}")