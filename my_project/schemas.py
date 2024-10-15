# schemas.py
from pydantic import BaseModel

class DetectionDataBase(BaseModel):
    image_path: str
    class_name: str
    confidence: float
    x_min: float
    y_min: float
    x_max: float
    y_max: float

class DetectionDataCreate(DetectionDataBase):
    pass

class DetectionData(DetectionDataBase):
    id: int

    class Config:
        orm_mode = True