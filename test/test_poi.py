import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import logging
from main import app
from app.database import Base
from app.services.databaseService import DatabaseService
from app import models, schemas

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create test database engine
SQLALCHEMY_DATABASE_URL = "sqlite:///./testdb.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Create TestingSessionLocal class
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
##adiciones

Base.metadata.create_all(bind=engine)
# Dependency override
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[DatabaseService.get_db] = override_get_db

client = TestClient(app)

##adiciones

@pytest.fixture(scope="session")
def db():
    """
    Fixture that creates a test database session that persists across all tests
    """
    logger.info("Iniciando configuración de base de datos de prueba")
    Base.metadata.create_all(bind=engine)
    
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)
        logger.info("Cerrando conexión a base de datos de prueba")

@pytest.fixture(scope="module")
def client():
    logger.info("Iniciando cliente de prueba")
    return TestClient(app)

@pytest.fixture
def sample_poi_data():
    return {
        "nombre": "Cascada El Saltillo",
        "descripcion": "Hermosa cascada natural",
        "foto_url": "http://ejemplo.com/cascada.jpg",
        "tipo": "Natural",
        "longitud": "-98.8765",
        "latitud": "19.4321"
    }

@pytest.mark.describe("Suite de pruebas CRUD para Puntos de Interés")
class TestPOICrud:
    
    @pytest.mark.it("Debe crear y leer un POI correctamente")
    def test_create_and_read_poi(self, client, db, sample_poi_data):
        """
        ID de la prueba: POI_CRUD_001
        Descripción: Prueba integrada de creación y lectura de POI
        """
        logger.info("\n=== Iniciando prueba de creación y lectura de POI ===")
        
        # Create POI
        logger.info(f"Creando POI con datos: {sample_poi_data}")
        response = client.post("/poi/createPois", json=sample_poi_data)
        assert response.status_code == 200, "Error al crear POI"
        created_poi = response.json()
        poi_id = created_poi["id"]
        logger.info(f"POI creado exitosamente con ID: {poi_id}")

        # Verify POI was created correctly
        logger.info(f"Verificando POI creado con ID: {poi_id}")
        response = client.get(f"/poi/getPoiById/{poi_id}")
        assert response.status_code == 200, "Error al obtener POI creado"
        retrieved_poi = response.json()
        
        # Verificaciones detalladas
        for key in ["nombre", "descripcion", "foto_url", "tipo", "longitud", "latitud"]:
            assert retrieved_poi[key] == sample_poi_data[key], f"El campo {key} no coincide"
            logger.info(f"✓ Campo {key} verificado correctamente")

        logger.info("=== Prueba de creación y lectura completada exitosamente ===\n")

    @pytest.mark.it("Debe obtener todos los POIs con paginación")
    def test_get_all_pois(self, client, db):
        """
        ID de la prueba: POI_CRUD_002
        Descripción: Obtener todos los POIs con paginación
        """
        logger.info("\n=== Iniciando prueba de obtención de POIs con paginación ===")
        
        # Get all POIs
        logger.info("Obteniendo todos los POIs (límite 10)")
        response = client.get("/poi/getAllPois?skip=0&limit=10")
        assert response.status_code == 200, "Error al obtener todos los POIs"
        pois = response.json()
        logger.info(f"Se obtuvieron {len(pois)} POIs")
        
        # Test pagination
        logger.info("Probando paginación (límite 5)")
        response = client.get("/poi/getAllPois?skip=0&limit=5")
        assert response.status_code == 200, "Error al obtener POIs paginados"
        pois_paginated = response.json()
        logger.info(f"Se obtuvieron {len(pois_paginated)} POIs en la página")
        assert len(pois_paginated) <= 5, "La paginación excede el límite especificado"

        logger.info("=== Prueba de paginación completada exitosamente ===\n")

    @pytest.mark.it("Debe manejar correctamente la búsqueda por ID")
    def test_get_poi_by_id(self, client, db):
        """
        ID de la prueba: POI_CRUD_003
        Descripción: Obtener POI por ID existente y no existente
        """
        logger.info("\n=== Iniciando prueba de búsqueda por ID ===")
        
        # Test with non-existent POI
        logger.info("Probando búsqueda de POI no existente")
        response = client.get("/poi/getPoiById/999999")
        assert response.status_code == 404, "Se esperaba error 404 para POI no existente"
        assert response.json()["detail"] == "POI not found"
        logger.info("✓ Manejo correcto de POI no existente")

        # Test with existing POI
        logger.info("Probando búsqueda de POI existente")
        response = client.get("/poi/getAllPois?limit=1")
        pois = response.json()
        if pois:
            poi_id = pois[0]["id"]
            logger.info(f"Buscando POI con ID: {poi_id}")
            response = client.get(f"/poi/getPoiById/{poi_id}")
            assert response.status_code == 200, "Error al obtener POI existente"
            poi_data = response.json()
            logger.info(f"POI encontrado: {poi_data['nombre']}")

        logger.info("=== Prueba de búsqueda por ID completada exitosamente ===\n")

    @pytest.mark.it("Debe validar correctamente datos inválidos")
    def test_create_poi_validation(self, client, db):
        """
        ID de la prueba: POI_CRUD_004
        Descripción: Validar creación de POI con datos inválidos
        """
        logger.info("\n=== Iniciando prueba de validación de datos ===")
        
        invalid_data = {
            "nombre": "POI Incompleto"
        }
        logger.info(f"Intentando crear POI con datos inválidos: {invalid_data}")
        response = client.post("/poi/createPois", json=invalid_data)
        assert response.status_code == 422, "Se esperaba error 422 para datos inválidos"
        logger.info("✓ Validación correcta de datos inválidos")
        
        logger.info("=== Prueba de validación completada exitosamente ===\n")

    @pytest.mark.it("Debe eliminar POI correctamente")
    def test_delete_poi(self, client, db, sample_poi_data):
        """
        ID de la prueba: POI_CRUD_005
        Descripción: Eliminar POI existente
        """
        logger.info("\n=== Iniciando prueba de eliminación de POI ===")
        
        # Create a POI to delete
        logger.info("Creando POI para eliminar")
        response = client.post("/poi/createPois", json=sample_poi_data)
        assert response.status_code == 200, "Error al crear POI para eliminar"
        poi_id = response.json()["id"]
        logger.info(f"POI creado con ID: {poi_id}")

        # Delete the POI
        logger.info(f"Eliminando POI con ID: {poi_id}")
        response = client.delete(f"/poi/deletePoisById/{poi_id}")
        assert response.status_code == 200, "Error al eliminar POI"
        assert response.json()["message"] == "POI deleted"
        logger.info("POI eliminado exitosamente")

        # Verify POI was deleted
        logger.info("Verificando que el POI fue eliminado")
        response = client.get(f"/poi/getPoiById/{poi_id}")
        assert response.status_code == 404, "El POI no fue eliminado correctamente"
        logger.info("✓ Se confirmó que el POI fue eliminado")

        logger.info("=== Prueba de eliminación completada exitosamente ===\n")