# app/models/sql_models.py
from sqlalchemy import Column, String, Integer, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

Base = declarative_base()

def generate_uuid():
    return str(uuid.uuid4())

class User(Base):
    __tablename__ = "users"
    
    id = Column(String, primary_key=True, default=generate_uuid)
    email = Column(String, unique=True, index=True, nullable=False)
    full_name = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(String, default="customer")  # customer, support_agent, admin
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    tickets = relationship("Ticket", back_populates="customer", foreign_keys="Ticket.customer_id")
    assigned_tickets = relationship("Ticket", back_populates="assigned_agent", foreign_keys="Ticket.assigned_agent_id")

class Ticket(Base):
    __tablename__ = "tickets"
    
    id = Column(String, primary_key=True, default=generate_uuid)
    customer_id = Column(String, ForeignKey("users.id"), nullable=False)
    assigned_agent_id = Column(String, ForeignKey("users.id"), nullable=True)
    subject = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    status = Column(String, default="open")  # open, in_progress, resolved, closed
    urgency = Column(Integer, default=1)  # 1-5 scale
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # AI Analysis fields
    ai_urgency = Column(Integer, nullable=True)
    ai_sentiment = Column(String, nullable=True)
    ai_sentiment_score = Column(Integer, nullable=True)
    ai_category = Column(String, nullable=True)
    ai_confidence = Column(Integer, nullable=True)
    
    # Relationships
    customer = relationship("User", back_populates="tickets", foreign_keys=[customer_id])
    assigned_agent = relationship("User", back_populates="assigned_tickets", foreign_keys=[assigned_agent_id])