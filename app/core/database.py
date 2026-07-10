from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from app.core.config import settings

# Create database engine
engine = create_engine(
    settings.SQLALCHEMY_DATABASE_URI,
    # pool_pre_ping=True helps handle dropped connections
    pool_pre_ping=True
)
# Create SessionLocal class which will be used to create database sessions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create declarative base class for all models
Base = declarative_base()

# Dependency to get database session has been moved to app/api/deps.py for cleaner architecture.
print("sucessfull")