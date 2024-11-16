from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import crud, schemas
from ..services.databaseService import DatabaseService

router = APIRouter(prefix="/flora",tags=["Flora"])


database_service = DatabaseService()

@router.get("/getAllFlora", response_model=list[schemas.Flora])
def read_flora(skip: int = 0, limit: int = 10, db: Session = Depends(database_service.get_db)):
    flora = crud.get_flora(db, skip=skip, limit=limit)
    return flora

@router.get("/getFloraById/{flora_id}", response_model=schemas.Flora)
def read_flora_by_id(flora_id: int, db: Session = Depends(database_service.get_db)):
    db_flora = crud.get_flora_by_id(db, flora_id=flora_id)
    if db_flora is None:
        raise HTTPException(status_code=404, detail="Flora not found")
    return db_flora

@router.post("/flora/", response_model=schemas.Flora)
def create_flora(flora: schemas.FloraCreate, db: Session = Depends(database_service.get_db)):
    # Verificar si el POI existe
    poi = crud.get_poi_by_id(db, flora.poi_id)
    if poi is None:
        raise HTTPException(status_code=404, detail="No se encontro el Punto de interes con el id {}".format(flora.poi_id))
    
    return crud.create_flora(db=db, flora=flora)

@router.delete("/flora/{flora_id}")
def delete_flora(flora_id: int, db: Session = Depends(database_service.get_db)):
    crud.delete_flora(db=db, flora_id=flora_id)
    return {"message": "Flora deleted"}