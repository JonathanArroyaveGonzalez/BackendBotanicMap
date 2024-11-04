from fastapi import FastAPI
from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from .routers import poi, flora, fauna
from .database import Base,engine
from . import models

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

Base.metadata.create_all(bind= engine)
app.include_router(poi.router)
app.include_router(flora.router)
app.include_router(fauna.router)

@app.get(
        "/healthCheck",
        status_code=status.HTTP_200_OK
        )
async def healthCheck():
    '''app is already working!'''
    return {"message": "All works!"}


