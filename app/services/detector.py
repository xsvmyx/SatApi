from app.detectors.Yolov8 import Yolov8
from app.utils.image_utils import decode_image
from app.utils.PredictRequest import PredictRequest
from fastapi.responses import JSONResponse
# model_map = {
#     "yolov8": Yolov8(),  
# }


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

         
            boxes.append({
                "x1": x1, "y1": y1,
                "x2": x2, "y2": y2,
                "class": cls_id
            })

        return JSONResponse(content={"bboxes": boxes})

    except ValueError as ve:
        logging.error(f"ValueError PUNAISE!!! : {str(ve)}")
        raise ve
    except Exception as e:
        logging.error(f"Erreur dans detect_image: {str(e)}")
        raise e