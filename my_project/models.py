# models.py
from sqlalchemy import Column, Integer, String, Float
from .database import Base

class DetectionData(Base):
    __tablename__ = "detection_data"

    id = Column(Integer, primary_key=True, index=True)
    image_path = Column(String, index=True)
    class_name = Column(String, index=True)
    confidence = Column(Float)
    x_min = Column(Float)
    y_min = Column(Float)
    x_max = Column(Float)
    y_max = Column(Float)