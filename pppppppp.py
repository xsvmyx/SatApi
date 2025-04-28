# from flask import Flask, request, jsonify
# from flask_cors import CORS
# from ultralytics import YOLO
# from PIL import Image
# import base64
# from io import BytesIO

# app = Flask(name)
# CORS(app)

# model = YOLO("runs/detect/train16/weights/best.pt")

# def decode_image(data_url):
#     # enlève "data:image/png;base64," et décode
#     header, encoded = data_url.split(",", 1)
#     img_bytes = base64.b64decode(encoded)
#     return Image.open(BytesIO(img_bytes))

# @app.route("/predict", methods=["POST"])
# def predict():
#     payload = request.json
#     img = decode_image(payload["image"])
#     w, h = img.size

#     # bornes géographiques
#     lat_top    = payload["latTop"]
#     lat_bottom = payload["latBottom"]
#     lon_left   = payload["lonLeft"]
#     lon_right  = payload["lonRight"]

#     # prédiction
#     results = model(img)[0]

#     boxes = []
#     for box in results.boxes:
#         x1, y1, x2, y2 = box.xyxy[0].tolist()
#         cls_id = int(box.cls[0])

#         # conversion pixel->latlon
#         lat1 = lat_top    + (y1 / h) * (lat_bottom - lat_top)
#         lon1 = lon_left   + (x1 / w) * (lon_right  - lon_left)
#         lat2 = lat_top    + (y2 / h) * (lat_bottom - lat_top)
#         lon2 = lon_left   + (x2 / w) * (lon_right  - lon_left)

#         boxes.append({
#             "lat1": lat1, "lon1": lon1,
#             "lat2": lat2, "lon2": lon2,
#             "class": cls_id
#         })

#     return jsonify({"bboxes": boxes})

# if name == "main":
#     app.run(debug=True)