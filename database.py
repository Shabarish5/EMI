import os
from dotenv import load_dotenv
from sqlmodel import SQLModel, create_engine, Session

# 1. Load environment variables
load_dotenv()

# 2. Get the URL
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL is not set in the .env file")

# --- THE FIX IS HERE ---
# SQLAlchemy requires 'postgresql://', but Neon gives 'postgres://'
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)
# -----------------------

# 3. Create the Postgres Engine
engine = create_engine(DATABASE_URL)

def create_db_and_tables():
    """Creates tables if they don't exist"""
    SQLModel.metadata.create_all(engine)

def get_session():
    """Dependency for FastAPI to get a DB session"""
    with Session(engine) as session:
        yield session
