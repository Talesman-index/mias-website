import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# The Neon.tech PostgreSQL connection string
DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "postgresql://neondb_owner:npg_ZNVbjt5JFc2i@ep-summer-leaf-b4eh0top-pooler.c-6.us-east-2.aws.neon.tech/neondb?sslmode=require"
)

# Create the SQLAlchemy Engine
engine = create_engine(DATABASE_URL)

# Create a SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a Base class for models
Base = declarative_base()

# Dependency to get the DB session in FastAPI
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
