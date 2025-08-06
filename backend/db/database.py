import os
import logging
from functools import wraps
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Row
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

POSTGRES_USER = os.getenv('POSTGRES_USER')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
POSTGRES_DB = os.getenv('POSTGRES_DB')
POSTGRES_HOST = os.getenv('POSTGRES_HOST')
POSTGRES_PORT = os.getenv('POSTGRES_PORT')

DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

# Create a SQLAlchemy engine
engine = create_engine(DATABASE_URL)

Base = declarative_base()
# Create a SessionLocal class

def get_db():
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    return db

def with_db(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        db = SessionLocal()
        try:
            return f(*args, db)
        finally:
            db.close()
    return decorated_function

def execute_query(query):
    con = engine.connect()
    try:
        result = con.execute(text(query))

        rows = [tuple(row) for row in result]
        return rows
    except Exception as e:
        raise e
