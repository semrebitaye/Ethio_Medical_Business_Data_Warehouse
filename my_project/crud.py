# crud.py
from sqlalchemy.orm import Session
from . import models, schemas

def get_detection_data(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.DetectionData).offset(skip).limit(limit).all()

def create_detection_data(db: Session, detection_data: schemas.DetectionDataCreate):
    db_detection_data = models.DetectionData(**detection_data.dict())
    db.add(db_detection_data)
    db.commit()
    db.refresh(db_detection_data)
    return db_detection_data