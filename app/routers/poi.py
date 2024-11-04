from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import crud, schemas
from ..database import SessionLocal

router = APIRouter(prefix="/pio",tags=["Punto de Interes"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/getAllPois", response_model=list[schemas.POI])
def read_pois(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    pois = crud.get_pois(db, skip=skip, limit=limit)
    return pois


@router.get("/getPoiById/{poi_id}", response_model=schemas.POI)
def read_poi_by_id(poi_id: int, db: Session = Depends(get_db)):
    db_poi = crud.get_poi_by_id(db, poi_id=poi_id)
    if db_poi is None:
        raise HTTPException(status_code=404, detail="POI not found")
    return db_poi


@router.post("/createPois", response_model=schemas.POI)
def create_poi(poi: schemas.POICreate, db: Session = Depends(get_db)):
    return crud.create_poi(db=db, poi=poi)

@router.delete("/deletePoisById/{poi_id}")
def delete_poi(poi_id: int, db: Session = Depends(get_db)):
    crud.delete_poi(db=db, poi_id=poi_id)
    return {"message": "POI deleted"}
