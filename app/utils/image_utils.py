import io
import numpy as np
from PIL import Image
from fastapi import UploadFile
import base64
from io import BytesIO

async def read_image(uploaded_file: UploadFile) -> np.ndarray:
    try:
        contents = await uploaded_file.read()
        image = Image.open(io.BytesIO(contents)).convert("RGB")
        image_np = np.array(image)
        return image_np
    except Exception as e:
        raise ValueError(f"Erreur lors de la lecture de l'image : {e}")
    


def decode_image(data_url):
    try:
        # Enlève "data:image/png;base64," et décode
        header, encoded = data_url.split(",", 1)
        img_bytes = base64.b64decode(encoded)
        img = Image.open(BytesIO(img_bytes))
        return img
    except Exception as e:
        # Si une erreur se produit, logge l'erreur et renvoie une exception
        raise ValueError(f"Erreur lors de la décodification de l'image: {str(e)}")