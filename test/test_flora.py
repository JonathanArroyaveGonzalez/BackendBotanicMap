import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import logging
from main import app
from app.database import Base
from app.services.databaseService import DatabaseService

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create test database engine
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Create TestingSessionLocal class
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

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
    Fixture that creates a test database session
    """
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="module")
def client():
    """
    Fixture that creates a test client
    """
    return TestClient(app)

logger = logging.getLogger(__name__)

@pytest.fixture
def sample_poi_data():
    return {
        "nombre": "Jardín Botánico",
        "descripcion": "Área de conservación de flora",
        "foto_url": "http://ejemplo.com/jardin.jpg",
        "tipo": "Natural",
        "longitud": "-99.1234",
        "latitud": "19.4321"
    }

@pytest.fixture
def sample_flora_data():
    return {
        "nombre_cientifico": "Dahlia coccinea",
        "nombre_comun": "Dalia",
        "familia": "Asteraceae",
        "foto_url": "http://ejemplo.com/dalia.jpg",
        "poi_id": 1
    }

@pytest.mark.describe("Suite de pruebas CRUD para Flora")
class TestFloraCrud:
    
    @pytest.mark.it("Debe crear y leer flora correctamente")
    def test_create_and_read_flora(self, client, db, sample_poi_data, sample_flora_data):
        """
        ID de la prueba: FLORA_CRUD_001
        Descripción: Prueba integrada de creación y lectura de flora
        Entradas:
            - POI válido para asociar con la flora
            - Datos de flora válidos completos
        Acciones:
            1. Crear un POI
            2. Crear un registro de flora asociado al POI
            3. Verificar la creación mediante lectura
        Resultados esperados:
            - Código 200 en la creación del POI y flora
            - Datos guardados coinciden con los enviados
            - Flora correctamente asociada al POI
            - Todos los campos mantienen su integridad
        """
        logger.info("\n=== Iniciando prueba de creación y lectura de flora ===")
        
        # Create POI first
        response = client.post("/poi/createPois", json=sample_poi_data)
        assert response.status_code == 200, "Error al crear POI"
        poi_response = response.json()
        poi_id = poi_response["id"]
        sample_flora_data["poi_id"] = poi_id
        
        # Create Flora
        response = client.post("/flora/flora/", json=sample_flora_data)
        assert response.status_code == 200, "Error al crear flora"
        created_flora = response.json()
        flora_id = created_flora["id"]
        
        # Verify flora was created correctly
        response = client.get(f"/flora/getFloraById/{flora_id}")
        assert response.status_code == 200, "Error al obtener flora creada"
        retrieved_flora = response.json()
        
        for key in ["nombre_cientifico", "nombre_comun", "familia", "foto_url"]:
            assert retrieved_flora[key] == sample_flora_data[key], f"El campo {key} no coincide"

    @pytest.mark.it("Debe obtener todas las floras con paginación")
    def test_get_all_flora(self, client, db):
        """
        ID de la prueba: FLORA_CRUD_002
        Descripción: Prueba de obtención de registros de flora con paginación
        Entradas:
            - Parámetros de paginación (skip=0, limit=10)
            - Parámetros de paginación reducida (skip=0, limit=5)
        Acciones:
            1. Solicitar lista completa de flora con límite de 10
            2. Solicitar lista con límite reducido de 5
            3. Verificar que la paginación funciona correctamente
        Resultados esperados:
            - Código 200 en ambas solicitudes
            - Lista completa respeta el límite de 10
            - Lista reducida respeta el límite de 5
            - Formato de respuesta correcto en ambos casos
        """
        logger.info("\n=== Iniciando prueba de obtención de flora con paginación ===")
        
        response = client.get("/flora/getAllFlora?skip=0&limit=10")
        assert response.status_code == 200, "Error al obtener toda la flora"
        flora_list = response.json()
        
        # Test pagination
        response = client.get("/flora/getAllFlora?skip=0&limit=5")
        flora_paginated = response.json()
        assert len(flora_paginated) <= 5, "La paginación excede el límite especificado"

    @pytest.mark.it("Debe manejar correctamente la búsqueda por ID")
    def test_get_flora_by_id(self, client, db):
        """
        ID de la prueba: FLORA_CRUD_003
        Descripción: Prueba de búsqueda de flora por ID existente y no existente
        Entradas:
            - ID de flora no existente (999999)
            - ID de flora existente (obtenido de la lista)
        Acciones:
            1. Intentar obtener flora con ID inexistente
            2. Obtener flora con ID existente
            3. Verificar respuestas en ambos casos
        Resultados esperados:
            - Código 404 para ID no existente
            - Código 200 para ID existente
            - Mensaje de error apropiado para ID no existente
            - Datos correctos para ID existente
        """
        logger.info("\n=== Iniciando prueba de búsqueda por ID ===")
        
        # Test with non-existent flora
        response = client.get("/flora/getFloraById/999999")
        assert response.status_code == 404, "Se esperaba error 404 para flora no existente"
        assert response.json()["detail"] == "Flora not found"

        # Test with existing flora
        response = client.get("/flora/getAllFlora?limit=1")
        flora_list = response.json()
        if flora_list:
            flora_id = flora_list[0]["id"]
            response = client.get(f"/flora/getFloraById/{flora_id}")
            assert response.status_code == 200, "Error al obtener flora existente"

    @pytest.mark.it("Debe validar correctamente datos inválidos")
    def test_create_flora_validation(self, client, db):
        """
        ID de la prueba: FLORA_CRUD_004
        Descripción: Prueba de validación de datos en la creación de flora
        Entradas:
            - Datos incompletos de flora (faltantes campos requeridos)
            - Datos completos pero con POI inexistente
        Acciones:
            1. Intentar crear flora con datos incompletos
            2. Intentar crear flora con POI no existente
            3. Verificar manejo de errores
        Resultados esperados:
            - Código 422 para datos incompletos
            - Código 404 para POI no existente
            - Mensajes de error descriptivos
        """
        logger.info("\n=== Iniciando prueba de validación de datos ===")
        
        invalid_data = {
            "nombre_comun": "Flora Incompleta",
            "poi_id": 1
        }
        response = client.post("/flora/flora/", json=invalid_data)
        assert response.status_code == 422, "Se esperaba error 422 para datos inválidos"
        
        complete_data = {
            "nombre_cientifico": "Test Plant",
            "nombre_comun": "Test Flora",
            "familia": "Test Family",
            "foto_url": "http://test.com/foto.jpg",
            "poi_id": 999999
        }
        response = client.post("/flora/flora/", json=complete_data)
        assert response.status_code == 404, "Se esperaba error 404 para POI no existente"

    @pytest.mark.it("Debe eliminar flora correctamente")
    def test_delete_flora(self, client, db, sample_poi_data, sample_flora_data):
        """
        ID de la prueba: FLORA_CRUD_005
        Descripción: Prueba de eliminación de registro de flora
        Entradas:
            - POI válido para la prueba
            - Datos de flora válidos para crear y eliminar
        Acciones:
            1. Crear POI de prueba
            2. Crear flora de prueba
            3. Eliminar flora creada
            4. Verificar que la flora fue eliminada
        Resultados esperados:
            - Código 200 en la creación del POI y flora
            - Código 200 en la eliminación
            - Código 404 al intentar obtener la flora eliminada
            - Mensaje de confirmación de eliminación
        """
        logger.info("\n=== Iniciando prueba de eliminación de flora ===")
        
        # Create POI and flora to delete
        response = client.post("/poi/createPois", json=sample_poi_data)
        assert response.status_code == 200, "Error al crear POI"
        poi_id = response.json()["id"]
        sample_flora_data["poi_id"] = poi_id
        
        response = client.post("/flora/flora/", json=sample_flora_data)
        assert response.status_code == 200, "Error al crear flora"
        flora_id = response.json()["id"]

        # Delete the flora
        response = client.delete(f"/flora/flora/{flora_id}")
        assert response.status_code == 200, "Error al eliminar flora"
        assert response.json()["message"] == "Flora deleted"

        # Verify flora was deleted
        response = client.get(f"/flora/getFloraById/{flora_id}")
        assert response.status_code == 404, "La flora no fue eliminada correctamente"