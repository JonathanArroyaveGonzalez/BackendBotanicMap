from sqlalchemy.orm import Session
from ..database import SessionLocal

class DatabaseService:
    """
    Clase para gestionar la interacción con la base de datos usando SQLAlchemy.
    """

    @staticmethod
    def get_db():
        """
        Generador que proporciona una sesión de base de datos.
        Esto asegura que la sesión se abra y cierre adecuadamente.
        """
        db = SessionLocal()
        try:
            yield db
        finally:
            db.close()