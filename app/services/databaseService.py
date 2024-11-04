from sqlalchemy.orm import Session
from ..database import SessionLocal

class DatabaseService:
    def __init__(self):
        self.db = None

    def get_db(self):
        self.db = SessionLocal()
        try:
            yield self.db
        finally:
            self.db.close()