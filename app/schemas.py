from pydantic import BaseModel

class POIBase(BaseModel):
    nombre: str
    descripcion: str
    foto_url: str
    tipo: str
    longitud: str
    latitud: str

class POICreate(POIBase):
    pass

class POI(POIBase):
    id: int

    class Config:
        from_attributes = True

class FloraBase(BaseModel):
    nombre_cientifico: str
    familia: str

class FloraCreate(FloraBase):
    pass

class Flora(FloraBase):
    id: int
    poi_id: int

    class Config:
        from_attributes = True

class FaunaBase(BaseModel):
    especie: str
    nombre_comun: str
    habitat: str

class FaunaCreate(FaunaBase):
    pass

class Fauna(FaunaBase):
    id: int
    poi_id: int

    class Config:
        from_attributes = True
