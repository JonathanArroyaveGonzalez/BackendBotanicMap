from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import crud, schemas
from ..services.databaseService import DatabaseService


router = APIRouter(prefix="/fauna",tags=["Fauna"])

database_service = DatabaseService()

@router.get("/getAllFauna", response_model=list[schemas.Fauna])
def read_fauna(skip: int = 0, limit: int = 10, db: Session = Depends(database_service.get_db)):
    fauna = crud.get_fauna(db, skip=skip, limit=limit)
    return fauna

@router.get("/getFaunaById/{fauna_id}", response_model=schemas.Fauna)
def read_fauna_by_id(fauna_id: int, db: Session = Depends(database_service.get_db)):
    db_fauna = crud.get_fauna_by_id(db, fauna_id=fauna_id)
    if db_fauna is None:
        raise HTTPException(status_code=404, detail="Fauna not found")
    return db_fauna

@router.post("/createFauna", response_model=schemas.Fauna)
def create_fauna(fauna: schemas.FaunaCreate, db: Session = Depends(database_service.get_db)):
    return crud.create_fauna(db=db, fauna=fauna)

@router.delete("/deleteFaunaById/{fauna_id}")
def delete_fauna(fauna_id: int, db: Session = Depends(database_service.get_db)):
    crud.delete_fauna(db=db, fauna_id=fauna_id)
    return {"message": "Fauna deleted"}