from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:postgresql2022@localhost:5432/sample'
SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:postgresql2022@db:5432/sample'

engine = create_engine(
    SQLALCHEMY_DATABASE_URL#, connect_args={'check_same_thread': False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
