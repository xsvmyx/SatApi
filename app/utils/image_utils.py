import io
import numpy as np
from PIL import Image
from fastapi import UploadFile
import base64
import requests
from io import BytesIO
import math
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
    




def latlon_to_tile(lat, lon, zoom):
    lat_rad = math.radians(lat)
    n = 2.0 ** zoom
    x_tile = int((lon + 180.0) / 360.0 * n)
    y_tile = int((1.0 - math.log(math.tan(lat_rad) + 1.0 / math.cos(lat_rad)) / math.pi) / 2.0 * n)
    return x_tile, y_tile


def build_maptiler_url(lat, lon, radius, token):
    # Convert radius to zoom level
    #zoom = 16 if radius == 1 else 15 if radius == 2 else 14 if radius == 3 else 13
    zoom = 16
    x, y = latlon_to_tile(lat, lon, zoom)
   
    return (
         f"https://api.maptiler.com/maps/satellite/{zoom}/{x}/{y}@2x.jpg?key={token}"
    )


def download_maptiler_image(url, save_path="bts_image.png"):
    
    response = requests.get(url)

    if response.status_code == 200:
        with open(save_path, "wb") as f:
            f.write(response.content)
        print(f"✅ Image enregistrée sous {save_path}")
    else:
        print(f"❌ Échec du téléchargement : {response.status_code} - {response.text}")






def build_mapbox_url(lat, lon, radius, token):
    
    zoom_by_radius = {1: 16, 2: 15, 3: 14, 4: 13}
    zoom = zoom_by_radius.get(radius, 13)
    
    


    url = (
        f"https://api.mapbox.com/styles/v1/mapbox/satellite-v9/static/"
        f"{lon},{lat},{zoom},0/512x512@2x?access_token={token}"
    )
   
    return url



def download_mapbox_image(url, save_path="image_box.jpg"):
    
    response = requests.get(url)
    
    if response.status_code == 200:
        
        image = Image.open(io.BytesIO(response.content)).convert("RGB")
        
        image_np = np.array(image)
        
        if save_path:
            image.save(save_path)
            print(f"Image sauvegardée dans {save_path}")
        return image_np
    else:
        print(f"❌ Échec du téléchargement : {response.status_code}")
        return None







###############################################################################################


