from typing import List, Optional
from pydantic import BaseModel

# Flora schemas
class FloraBase(BaseModel):
    nombre_cientifico: str
    nombre_comun: str
    familia: str
    foto_url: str
    poi_id: int

class FloraCreate(FloraBase):
    pass

class Flora(FloraBase):
    id: int
    
    class Config:
        from_attributes = True

# Fauna schemas
class FaunaBase(BaseModel):
    nombre_cientifico: str
    nombre_comun: str
    especie: str
    habitat: str
    foto_url: str
    poi_id: int

class FaunaCreate(FaunaBase):
    pass

class Fauna(FaunaBase):
    id: int
    
    class Config:
        from_attributes = True

# POI schemas
class POIBase(BaseModel):
    nombre: str
    descripcion: str
    foto_url: str
    tipo: str
    longitud: str
    latitud: str

class POICreate(POIBase):
    pass

# POI response schema with relationships
class POI(POIBase):
    id: int
    flora: List[Flora] = []
    fauna: List[Fauna] = []
    
    class Config:
        from_attributes = True
