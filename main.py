import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi import status
from app.controllers import poi, flora, fauna, image
from app.database import Base, engine
from app.models import models

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Marketplace API",
    debug=True
)

# Configuración de CORS
origins = [
    "*",  # Permite solicitudes de cualquier origen
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(poi.router)
app.include_router(flora.router)
app.include_router(fauna.router)
app.include_router(image.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Marketplace API"}

@app.get(
        "/healthCheck",
        status_code=status.HTTP_200_OK
        )
async def healthCheck():
    '''app is already working!'''
    return {"message": "All works!"}


