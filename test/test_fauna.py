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

Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[DatabaseService.get_db] = override_get_db

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
        "nombre": "Bosque de Pinos",
        "descripcion": "Área natural protegida",
        "foto_url": "http://ejemplo.com/bosque.jpg",
        "tipo": "Natural",
        "longitud": "-99.1234",
        "latitud": "19.4321"
    }

@pytest.fixture
def sample_fauna_data():
    return {
        "nombre_cientifico": "Lynx rufus",
        "nombre_comun": "Gato montés",
        "especie": "Mamífero",
        "habitat": "Bosque templado",
        "foto_url": "http://ejemplo.com/lince.jpg",
        "poi_id": 1
    }

@pytest.mark.describe("Suite de pruebas CRUD para Fauna")
class TestFaunaCrud:
    
    @pytest.mark.it("Debe crear y leer fauna correctamente")
    def test_create_and_read_fauna(self, client, db, sample_poi_data, sample_fauna_data):
        """
        ID de la prueba: FAUNA_CRUD_001
        Descripción: Prueba integrada de creación y lectura de fauna
        Entradas:
            - POI válido para asociar con la fauna
            - Datos de fauna válidos
        Acciones:
            1. Crear un POI
            2. Crear un registro de fauna asociado al POI
            3. Verificar la creación mediante lectura
        Resultados esperados:
            - Código 200 en la creación
            - Datos guardados coinciden con los enviados
            - Fauna correctamente asociada al POI
        """
        logger.info("\n=== Iniciando prueba de creación y lectura de fauna ===")
        
        # Create POI first
        response = client.post("/poi/createPois", json=sample_poi_data)
        logger.info(f"Response al crear POI: {response.json()}")
        assert response.status_code == 200, "Error al crear POI"
        poi_response = response.json()
        assert "id" in poi_response, "La respuesta no contiene 'id'"
        poi_id = poi_response["id"]
        sample_fauna_data["poi_id"] = poi_id
        
        # Create Fauna
        logger.info(f"Creando fauna con datos: {sample_fauna_data}")
        response = client.post("/fauna/createFauna", json=sample_fauna_data)
        logger.info(f"Response al crear fauna: {response.json()}")
        assert response.status_code == 200, "Error al crear fauna"
        created_fauna = response.json()
        fauna_id = created_fauna["id"]
        logger.info(f"Fauna creada exitosamente con ID: {fauna_id}")

        # Verify fauna was created correctly
        response = client.get(f"/fauna/getFaunaById/{fauna_id}")
        logger.info(f"Response al obtener fauna creada: {response.json()}")
        assert response.status_code == 200, "Error al obtener fauna creada"
        retrieved_fauna = response.json()
        
        for key in ["nombre_cientifico", "nombre_comun", "especie", "habitat", "foto_url"]:
            assert retrieved_fauna[key] == sample_fauna_data[key], f"El campo {key} no coincide"
            logger.info(f"✓ Campo {key} verificado correctamente")

    @pytest.mark.it("Debe obtener todas las faunas con paginación")
    def test_get_all_fauna(self, client, db):
        """
        ID de la prueba: FAUNA_CRUD_002
        Descripción: Obtener todos los registros de fauna con paginación
        Entradas:
            - Parámetros de paginación (skip=0, limit=10)
        Acciones:
            1. Solicitar lista de fauna con diferentes límites
            2. Verificar la paginación
        Resultados esperados:
            - Código 200
            - Lista de fauna respeta límites de paginación
            - Formato correcto de respuesta
        """
        logger.info("\n=== Iniciando prueba de obtención de fauna con paginación ===")
        
        response = client.get("/fauna/getAllFauna?skip=0&limit=10")
        assert response.status_code == 200, "Error al obtener toda la fauna"
        fauna_list = response.json()
        logger.info(f"Se obtuvieron {len(fauna_list)} registros de fauna")
        
        # Test pagination
        response = client.get("/fauna/getAllFauna?skip=0&limit=5")
        fauna_paginated = response.json()
        assert len(fauna_paginated) <= 5, "La paginación excede el límite especificado"
        logger.info("✓ Paginación verificada correctamente")

    @pytest.mark.it("Debe manejar correctamente la búsqueda por ID")
    def test_get_fauna_by_id(self, client, db):
        """
        ID de la prueba: FAUNA_CRUD_003
        Descripción: Obtener fauna por ID existente y no existente
        Entradas:
            - ID existente
            - ID no existente (999999)
        Acciones:
            1. Buscar fauna con ID no existente
            2. Buscar fauna con ID existente
        Resultados esperados:
            - 404 para ID no existente
            - 200 y datos correctos para ID existente
        """
        logger.info("\n=== Iniciando prueba de búsqueda por ID ===")
        
        # Test with non-existent fauna
        response = client.get("/fauna/getFaunaById/999999")
        assert response.status_code == 404, "Se esperaba error 404 para fauna no existente"
        assert response.json()["detail"] == "Fauna not found"
        logger.info("✓ Manejo correcto de fauna no existente")

        # Test with existing fauna
        response = client.get("/fauna/getAllFauna?limit=1")
        fauna_list = response.json()
        if fauna_list:
            fauna_id = fauna_list[0]["id"]
            response = client.get(f"/fauna/getFaunaById/{fauna_id}")
            assert response.status_code == 200, "Error al obtener fauna existente"
            logger.info("✓ Búsqueda de fauna existente correcta")

    @pytest.mark.it("Debe validar correctamente datos inválidos")
    def test_create_fauna_validation(self, client, db):
        """
        ID de la prueba: FAUNA_CRUD_004
        Descripción: Validar creación de fauna con datos inválidos
        Entradas:
            - Datos incompletos de fauna
            - POI ID no existente
        Acciones:
            1. Intentar crear fauna con datos incompletos
            2. Intentar crear fauna con POI inexistente
        Resultados esperados:
            - 422 para datos incompletos
            - 404 para POI no existente
        """
        logger.info("\n=== Iniciando prueba de validación de datos ===")
        
        invalid_data = {
            "nombre_comun": "Fauna Incompleta",
            "poi_id": 1
        }
        response = client.post("/fauna/createFauna", json=invalid_data)
        assert response.status_code == 422, "Se esperaba error 422 para datos inválidos"
        
        # Test with non-existent POI
        complete_data = {
            "nombre_cientifico": "Test Species",
            "nombre_comun": "Test Animal",
            "especie": "Test",
            "habitat": "Test Habitat",
            "foto_url": "http://test.com/foto.jpg",
            "poi_id": 999999
        }
        response = client.post("/fauna/createFauna", json=complete_data)
        assert response.status_code == 404, "Se esperaba error 404 para POI no existente"
        logger.info("✓ Validación de datos correcta")

    @pytest.mark.it("Debe eliminar fauna correctamente")
    def test_delete_fauna(self, client, db, sample_poi_data, sample_fauna_data):
        """
        ID de la prueba: FAUNA_CRUD_005
        Descripción: Eliminar fauna existente
        Entradas:
            - POI válido
            - Datos de fauna válidos
        Acciones:
            1. Crear POI y fauna para la prueba
            2. Eliminar fauna creada
            3. Verificar eliminación
        Resultados esperados:
            - 200 en la eliminación
            - 404 al intentar obtener la fauna eliminada
        """
        logger.info("\n=== Iniciando prueba de eliminación de fauna ===")
        
        # Create POI and fauna to delete
        response = client.post("/poi/createPois", json=sample_poi_data)
        logger.info(f"Response al crear POI: {response.json()}")
        assert response.status_code == 200, "Error al crear POI"
        poi_response = response.json()
        assert "id" in poi_response, "La respuesta no contiene 'id'"
        poi_id = poi_response["id"]
        sample_fauna_data["poi_id"] = poi_id
        
        response = client.post("/fauna/createFauna", json=sample_fauna_data)
        logger.info(f"Response al crear fauna: {response.json()}")
        fauna_id = response.json()["id"]
        logger.info(f"Fauna creada con ID: {fauna_id}")

        # Delete the fauna
        response = client.delete(f"/fauna/deleteFaunaById/{fauna_id}")
        logger.info(f"Response al eliminar fauna: {response.json()}")
        assert response.status_code == 200, "Error al eliminar fauna"
        assert response.json()["message"] == "Fauna deleted"
        logger.info("Fauna eliminada exitosamente")

        # Verify fauna was deleted
        response = client.get(f"/fauna/getFaunaById/{fauna_id}")
        logger.info(f"Response al verificar eliminación de fauna: {response.json()}")
        assert response.status_code == 404, "La fauna no fue eliminada correctamente"
        logger.info("✓ Se confirmó que la fauna fue eliminada")