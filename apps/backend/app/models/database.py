from sqlalchemy.pool import StaticPool
from sqlalchemy import Column, String, DateTime, Boolean, Text, Integer, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import os
from dotenv import load_dotenv
import uuid

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./support_triage.db")

Base = declarative_base()

def generate_uuid():
    return str(uuid.uuid4())

class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, default=generate_uuid, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    full_name = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(String, default="customer")
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(String, primary_key=True, default=generate_uuid, index=True)
    customer_id = Column(String, ForeignKey("users.id"), nullable=False)
    assigned_agent_id = Column(String, ForeignKey("users.id"), nullable=True)
    subject = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    status = Column(String, default="open")  # open, assigned, in_progress, resolved, closed
    urgency = Column(Integer, default=1)
    category = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    assigned_at = Column(DateTime, nullable=True)
    resolved_at = Column(DateTime, nullable=True)  # NEW: When ticket was resolved
    closed_at = Column(DateTime, nullable=True)    # NEW: When ticket was closed
    
    # AI Analysis Fields
    ai_urgency = Column(Integer)
    ai_sentiment = Column(String)
    ai_sentiment_score = Column(Integer)
    ai_category = Column(String)
    ai_confidence = Column(Integer)

    # Relationships
    customer = relationship("User", foreign_keys=[customer_id])
    assigned_agent = relationship("User", foreign_keys=[assigned_agent_id])

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# FORCE TABLE RECREATION
# print("DROPPING AND RECREATING ALL TABLES...")
# Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)
# print("TABLES RECREATED SUCCESSFULLY!")
