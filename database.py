import os
import json
from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 1. DATABASE CONNECTION
# Railway provides DATABASE_URL. We ensure it starts with postgresql:// for SQLAlchemy
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./face_db.sqlite")
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

# Connect to DB
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# 2. USER MODEL
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    
    # We store the embedding (a list of floats) as a massive text string
    # Postgres has ARRAY types, but TEXT is safer for compatibility between SQLite/Postgres
    embedding_json = Column(Text, nullable=False)

    # Helper to get the list back from the JSON string
    def get_embedding_list(self):
        if self.embedding_json:
            return json.loads(self.embedding_json)
        return []

    # Helper to set the JSON string from a list
    def set_embedding_list(self, embedding_list):
        self.embedding_json = json.dumps(embedding_list)

def init_db():
    Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
