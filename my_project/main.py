# main.py
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import crud, models, schemas, database

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

# Dependency
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/detection_data/", response_model=schemas.DetectionData)
def create_detection_data(detection_data: schemas.DetectionDataCreate, db: Session = Depends(get_db)):
    return crud.create_detection_data(db=db, detection_data=detection_data)

@app.get("/detection_data/", response_model=list[schemas.DetectionData])
def read_detection_data(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    detection_data = crud.get_detection_data(db, skip=skip, limit=limit)
    return detection_data