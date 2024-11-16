import os,ssl
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()
ssl_context = ssl.create_default_context()

SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")
#SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_TEST")

engine = create_engine(SQLALCHEMY_DATABASE_URL,connect_args={"ssl_context": ssl_context},)

#engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
