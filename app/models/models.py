from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from ..database import Base

class POI(Base):
    __tablename__ = "puntos_de_interes"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True)
    descripcion = Column(String)
    foto_url = Column(String)
    tipo = Column(String)
    longitud = Column(String)
    latitud = Column(String)

    flora = relationship("Flora", back_populates="poi")
    fauna = relationship("Fauna", back_populates="poi")

class Flora(Base):
    __tablename__ = "flora"

    id = Column(Integer, primary_key=True, index=True)
    nombre_cientifico = Column(String, index=True)
    nombre_comun = Column(String, index=True)
    familia = Column(String)
    foto_url = Column(String)
    poi_id = Column(Integer, ForeignKey('puntos_de_interes.id'))

    poi = relationship("POI", back_populates="flora")

class Fauna(Base):
    __tablename__ = "fauna"

    id = Column(Integer, primary_key=True, index=True)
    nombre_cientifico = Column(String, index=True)
    nombre_comun = Column(String)
    especie = Column(String, index=True)
    habitat = Column(String)
    foto_url = Column(String)
    poi_id = Column(Integer, ForeignKey('puntos_de_interes.id'))

    poi = relationship("POI", back_populates="fauna")
