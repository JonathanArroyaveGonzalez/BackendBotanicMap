from sqlalchemy.orm import Session
from . import  schemas
from .models import models


def get_pois(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.POI).offset(skip).limit(limit).all()

def get_poi_by_id(db: Session, poi_id: int):
    return db.query(models.POI).filter(models.POI.id == poi_id).first()

def create_poi(db: Session, poi: schemas.POICreate):
    db_poi = models.POI(**poi.model_dump())
    db.add(db_poi)
    db.commit()
    db.refresh(db_poi)
    return db_poi

def delete_poi(db: Session, poi_id: int):
    db.query(models.POI).filter(models.POI.id == poi_id).delete()
    db.commit()


def get_flora(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Flora).offset(skip).limit(limit).all()

def get_flora_by_id(db: Session, flora_id: int):
    return db.query(models.Flora).filter(models.Flora.id == flora_id).first()


def create_flora(db: Session, flora: schemas.FloraCreate):
    db_flora = models.Flora(**flora.model_dump())
    db.add(db_flora)
    db.commit()
    db.refresh(db_flora)
    return db_flora

def delete_flora(db: Session, flora_id: int):
    db.query(models.Flora).filter(models.Flora.id == flora_id).delete()
    db.commit()

def get_fauna(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Fauna).offset(skip).limit(limit).all()

def get_fauna_by_id(db: Session, fauna_id: int):
    return db.query(models.Fauna).filter(models.Fauna.id == fauna_id).first()


def create_fauna(db: Session, fauna: schemas.FaunaCreate):
    db_fauna = models.Fauna(**fauna.model_dump())
    db.add(db_fauna)
    db.commit()
    db.refresh(db_fauna)
    return db_fauna

def delete_fauna(db: Session, fauna_id: int):
    db.query(models.Fauna).filter(models.Fauna.id == fauna_id).delete()
    db.commit()