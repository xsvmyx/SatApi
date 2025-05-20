from pydantic import BaseModel
class PredictRequest(BaseModel):
    image: str  # image encodée en base64
    latTop: float
    latBottom: float
    lonLeft: float
    lonRight: float



class BTSpred(BaseModel):
    code: str
    model: str