from app.detectors.Yolov8 import Yolov8
from app.utils.image_utils import decode_image
from app.utils.Request import PredictRequest
from fastapi.responses import JSONResponse
# model_map = {
#     "yolov8": Yolov8(),  
# }

# async def detect_image(payload: PredictRequest):
#     img = decode_image(payload.image)
#     w, h = img.size

#     lat_top    = payload.latTop
#     lat_bottom = payload.latBottom
#     lon_left   = payload.lonLeft
#     lon_right  = payload.lonRight

#     model = Yolov8()
    
#     results  = model.detect(img)
    
#     boxes = []
#     for box in results.boxes:
#         xyxy = box.xyxy[0].tolist()  # Obtient la première valeur de xyxy comme liste
#         if len(xyxy) != 4:
#             raise ValueError(f"box.xyxy ne contient pas 4 éléments : {xyxy}")
    
#         x1, y1, x2, y2 = xyxy
#         cls_id = int(box.cls[0])

#         # conversion pixel -> latlon
#         lat1 = lat_top    + (y1 / h) * (lat_bottom - lat_top)
#         lon1 = lon_left   + (x1 / w) * (lon_right  - lon_left)
#         lat2 = lat_top    + (y2 / h) * (lat_bottom - lat_top)
#         lon2 = lon_left   + (x2 / w) * (lon_right  - lon_left)

#         boxes.append({
#             "lat1": lat1, "lon1": lon1,
#             "lat2": lat2, "lon2": lon2,
#             "class": cls_id
#         })

#     return JSONResponse(content={"bboxes": boxes})



import logging


logging.basicConfig(level=logging.DEBUG)

async def detect_image(payload: PredictRequest):
    try:
     
        img = decode_image(payload.image)
        w, h = img.size
        
        
        
        lat_top = payload.latTop
        lat_bottom = payload.latBottom
        lon_left = payload.lonLeft
        lon_right = payload.lonRight

        logging.debug(f"Geographical bounds: {lat_top}, {lat_bottom}, {lon_left}, {lon_right}")
        
       
        model = Yolov8()

      
        results = model.detect(img)
        
        
      
        boxes = []
        

        for box in results.boxes:
            
            
            xyxy = box.xyxy[0].tolist()  
            if len(xyxy) != 4:
                logging.error(f"Box.xyxy contient un nombre invalide d'éléments: {xyxy}")
                raise ValueError(f"box.xyxy ne contient pas 4 éléments : {xyxy}")
            
        x1, y1, x2, y2 = xyxy
        cls_id = int(box.cls[0])

        # conversion pixel -> latlon
        lat1 = lat_top    + (y1 / h) * (lat_bottom - lat_top)
        lon1 = lon_left   + (x1 / w) * (lon_right  - lon_left)
        lat2 = lat_top    + (y2 / h) * (lat_bottom - lat_top)
        lon2 = lon_left   + (x2 / w) * (lon_right  - lon_left)

        boxes.append({
            "lat1": lat1, "lon1": lon1,
            "lat2": lat2, "lon2": lon2,
            "class": cls_id
        })
        return JSONResponse(content={"bboxes": boxes})

    except ValueError as ve:
        logging.error(f"ValueError PUNAISE!!! : {str(ve)}")
        raise ve
    except Exception as e:
        logging.error(f"Erreur dans detect_image: {str(e)}")
        raise e