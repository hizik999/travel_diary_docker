from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv
from pathlib import Path

env_path = Path(__file__).resolve().parents[2] / '.env'
load_dotenv(dotenv_path=env_path)

POSTGRES_USER = os.getenv("fPOSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("fPOSTGRES_PASSWORD")
POSTGRES_DB = os.getenv("fPOSTGRES_DB")
POSTGRES_HOST_PORT = os.getenv("POSTGRES_HOST_PORT", "localhost:5432")

DATABASE_URL = f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST_PORT}/{POSTGRES_DB}"

fUSERNAME = os.getenv("fUSERNAME")
fPASSWORD = os.getenv("fPASSWORD")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()