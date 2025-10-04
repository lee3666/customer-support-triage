# app/api/main.py
from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
import uuid
from sqlalchemy.orm import Session
from sqlalchemy import text
import logging
import traceback

from app.models.database import get_db, Ticket, User, Base, engine
from app.services.ai_service import ai_service
from app.services.email_service import EmailService  # <-- EDIT 1: Added import
from app.workers.tasks import process_ticket_ai, send_email_notification, send_welcome_email

# Create FastAPI app FIRST
app = FastAPI(title="Customer Support Triage System", version="1.0.0")

# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    print(f"Global error: {exc}")
    print(f"Traceback: {traceback.format_exc()}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error", "error": str(exc)}
    )

# Test the exception handler
@app.get("/test-error")
async def test_error():
    raise Exception("This is a test error")

# Create tables
Base.metadata.create_all(bind=engine)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:3001",
        "http://localhost:3003",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:3001",
        "http://127.0.0.1:3003"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Import and include auth router AFTER creating the app and middleware
from app.api.auth import router as auth_router
app.include_router(auth_router, prefix="/auth", tags=["authentication"])

logger = logging.getLogger(__name__)

class TicketCreate(BaseModel):
    customer_id: str
    subject: str
    description: str

class TicketResponse(BaseModel):
    id: str
    customer_id: str
    subject: str
    description: str
    status: str
    urgency: int
    category: Optional[str] = None
    created_at: datetime

    # AI Analysis Fields
    ai_urgency: Optional[int] = None
    ai_sentiment: Optional[str] = None
    ai_sentiment_score: Optional[float] = None
    ai_category: Optional[str] = None
    ai_confidence: Optional[float] = None

    class Config:
        from_attributes = True

@app.get("/")
async def root():
    return {"message": "Customer Support Triage System API"}

@app.get("/health")
async def health_check(db: Session = Depends(get_db)):
    try:
        # Test database connection
        db.execute(text("SELECT 1"))
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        return {"status": "unhealthy", "database": "disconnected", "error": str(e)}

@app.post("/api/tickets", response_model=TicketResponse)
async def create_ticket(ticket: TicketCreate, db: Session = Depends(get_db)):
    ticket_id = str(uuid.uuid4())

    # AI Analysis
    print(f"Analyzing ticket with AI: {ticket.subject}")
    ai_analysis = ai_service.analyze_ticket(ticket.subject, ticket.description)
    print(f"AI Analysis Result: {ai_analysis}")
    
    db_ticket = Ticket(
        id=ticket_id,
        customer_id=ticket.customer_id,
        subject=ticket.subject,
        description=ticket.description,
        status="open",
        urgency=ai_analysis['urgency'],
        category=ai_analysis['category'],
        ai_urgency=ai_analysis['urgency'],
        ai_sentiment=ai_analysis['sentiment'],
        ai_sentiment_score=ai_analysis['sentiment_score'],
        ai_category=ai_analysis['category'],
        ai_confidence=ai_analysis['confidence']
    )

    db.add(db_ticket)
    db.commit()
    db.refresh(db_ticket)

    # ✅ EMAIL INTEGRATION: Get customer email and send notification  <-- EDIT 2: Added email integration
    customer = db.query(User).filter(User.id == ticket.customer_id).first()
    if customer and customer.email:
        try:
            EmailService.send_new_ticket_notification(db_ticket, customer.email)
            print(f"📧 Sent new ticket notification to: {customer.email}")
        except Exception as email_error:
            print(f"⚠️  Failed to send email: {email_error}")
            # Don't fail the ticket creation if email fails
    else:
        print("⚠️  No customer email found, skipping email notification")

    # BACKGROUND PROCESSING
    try:
        # Process ticket with advanced AI in background
        process_ticket_ai.delay(ticket_id)
        
        # Send welcome email to customer
        send_welcome_email.delay(f"{ticket.customer_id}@customer.com", f"Customer {ticket.customer_id}")
        
        # Notify agents about new ticket
        if ai_analysis['urgency'] >= 4:
            send_email_notification.delay(
                ticket_id,
                "HIGH PRIORITY - Ticket Created",
                f"High urgency ticket '{ticket.subject}' requires immediate attention."
            )
        else:
            send_email_notification.delay(
                ticket_id,
                "New Support Ticket Created", 
                f"New ticket '{ticket.subject}' has been created and is awaiting review."
            )

    except Exception as e:
        logger.error(f"Background task scheduling failed: {e}")
        # Non-critical, so don't fail the request

    return db_ticket

@app.get("/api/tickets", response_model=List[TicketResponse])
async def get_tickets(db: Session = Depends(get_db)):
    try:
        print("DEBUG: Starting get_tickets...")
        tickets = db.query(Ticket).order_by(Ticket.created_at.desc()).all()
        print(f"DEBUG: Found {len(tickets)} tickets")
        return tickets
    except Exception as e:
        print(f"DEBUG: Error in get_tickets: {e}")
        import traceback
        print(f"DEBUG: Traceback: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/tickets/{ticket_id}", response_model=TicketResponse)
async def get_ticket(ticket_id: str, db: Session = Depends(get_db)):
    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return ticket

# NEW ENDPOINT: Get AI analysis without creating ticket
@app.post("/api/analyze-ticket")
async def analyze_ticket_content(ticket: TicketCreate):
    """Analyze ticket content with AI without saving to database"""
    ai_analysis = ai_service.analyze_ticket(ticket.subject, ticket.description)
    return {
        "analysis": ai_analysis,
        "original_content": {
            "subject": ticket.subject,
            "description": ticket.description
        }
    }

# ============================================================================
# DASHBOARD ENDPOINTS
# ============================================================================

from datetime import timedelta

# Import the auth dependency
from app.core.auth import get_current_active_user

# Customer Dashboard Stats
@app.get("/api/dashboard/customer/stats")
async def get_customer_dashboard_stats(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    if current_user.role != "customer":
        raise HTTPException(status_code=403, detail="Not authorized")
    
    # Get customer's tickets
    tickets = db.query(Ticket).filter(Ticket.customer_id == current_user.id).all()
    
    stats = {
        "total_tickets": len(tickets),
        "open_tickets": len([t for t in tickets if t.status == "open"]),
        "in_progress_tickets": len([t for t in tickets if t.status == "in_progress"]),
        "resolved_tickets": len([t for t in tickets if t.status == "resolved"]),
        "recent_tickets": len([t for t in tickets if t.created_at > datetime.utcnow() - timedelta(days=7)])
    }
    
    return stats

# Customer Tickets
@app.get("/api/dashboard/customer/tickets")
async def get_customer_tickets(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    if current_user.role != "customer":
        raise HTTPException(status_code=403, detail="Not authorized")
    
    tickets = db.query(Ticket).filter(Ticket.customer_id == current_user.id).order_by(Ticket.created_at.desc()).all()
    
    return tickets

# Support Agent Dashboard Stats
@app.get("/api/dashboard/support-agent/stats")
async def get_support_agent_dashboard_stats(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    if current_user.role not in ["support_agent", "admin"]:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    # All tickets for support agents to see
    all_tickets = db.query(Ticket).all()
    assigned_tickets = db.query(Ticket).filter(Ticket.assigned_agent_id == current_user.id).all()
    unassigned_tickets = db.query(Ticket).filter(Ticket.assigned_agent_id == None).all()
    
    # Calculate stats
    today = datetime.utcnow().date()
    resolved_today = len([t for t in assigned_tickets if t.status == "resolved" and t.updated_at.date() == today])
    
    stats = {
        "total_tickets": len(all_tickets),
        "assigned_tickets": len(assigned_tickets),
        "unassigned_tickets": len(unassigned_tickets),
        "resolved_today": resolved_today,
        "avg_response_time": 45,
        "high_urgency_tickets": len([t for t in all_tickets if t.urgency >= 4]),
        "open_tickets": len([t for t in all_tickets if t.status == "open"]),
        "my_assigned_tickets": len(assigned_tickets)
    }
    
    return stats

# Support Agent Tickets
@app.get("/api/dashboard/support-agent/tickets")
async def get_support_agent_tickets(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    if current_user.role not in ["support_agent", "admin"]:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    # Support agents can see all tickets
    tickets = db.query(Ticket).order_by(Ticket.created_at.desc()).all()
    
    return tickets

# Admin Dashboard Stats
@app.get("/api/dashboard/admin/stats")
async def get_admin_dashboard_stats(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")
    
    users = db.query(User).all()
    tickets = db.query(Ticket).all()
    
    stats = {
        "total_users": len(users),
        "total_tickets": len(tickets),
        "active_tickets": len([t for t in tickets if t.status in ["open", "in_progress"]]),
        "support_agents": len([u for u in users if u.role == "support_agent"]),
        "customers": len([u for u in users if u.role == "customer"]),
        "tickets_this_week": len([t for t in tickets if t.created_at > datetime.utcnow() - timedelta(days=7)]),
        "resolution_rate": round(len([t for t in tickets if t.status == "resolved"]) / len(tickets) * 100, 2) if tickets else 0
    }
    
    return stats

# Get tickets by customer ID
@app.get("/api/tickets/customer/{customer_id}")
async def get_tickets_by_customer(
    customer_id: str,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    # Customers can only see their own tickets
    if current_user.role == "customer" and current_user.id != customer_id:
        raise HTTPException(status_code=403, detail="Can only view your own tickets")
    
    tickets = db.query(Ticket).filter(Ticket.customer_id == customer_id).order_by(Ticket.created_at.desc()).all()
    return tickets

# ============================================================================
# TICKET ASSIGNMENT ENDPOINTS
# ============================================================================

@app.post("/api/tickets/{ticket_id}/assign")
async def assign_ticket_to_agent(
    ticket_id: str,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    if current_user.role not in ["support_agent", "admin"]:
        raise HTTPException(status_code=403, detail="Only support agents and admins can assign tickets")
    
    # Get the ticket
    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    
    # Assign to current user
    ticket.assigned_agent_id = current_user.id
    ticket.status = "assigned"
    ticket.assigned_at = datetime.utcnow()
    
    db.commit()
    db.refresh(ticket)

    # ✅ EMAIL INTEGRATION: Send assignment notification
    try:
        # Get customer details
        customer = db.query(User).filter(User.id == ticket.customer_id).first()
        if customer and customer.email:
            EmailService.send_ticket_assigned_notification(ticket, current_user, customer.email)
            print(f"📧 Sent assignment notification to: {customer.email}")
        else:
            print("⚠️ No customer email found for assignment notification")
    except Exception as email_error:
        print(f"⚠️ Failed to send assignment email: {email_error}")
        # Don't fail the assignment if email fails
    
    return {
        "message": f"Ticket assigned to {current_user.full_name}",
        "ticket": ticket
    }

@app.post("/api/tickets/{ticket_id}/unassign")
async def unassign_ticket(
    ticket_id: str,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    if current_user.role not in ["support_agent", "admin"]:
        raise HTTPException(status_code=403, detail="Only support agents and admins can unassign tickets")
    
    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    
    # Only allow unassigning if the current user is the assigned agent or an admin
    if current_user.role != "admin" and ticket.assigned_agent_id != current_user.id:
        raise HTTPException(status_code=403, detail="Can only unassign tickets assigned to you")
    
    ticket.assigned_agent_id = None
    ticket.status = "open"
    ticket.assigned_at = None
    
    db.commit()
    db.refresh(ticket)
    
    return {
        "message": "Ticket unassigned",
        "ticket": ticket
    }

@app.get("/api/support-agents")
async def get_support_agents(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    if current_user.role not in ["support_agent", "admin"]:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    agents = db.query(User).filter(User.role == "support_agent").all()
    return agents

@app.get("/cors-test")
async def cors_test():
    return {"message": "CORS test successful", "cors_enabled": True}

# ============================================================================
# TICKET STATUS WORKFLOW ENDPOINTS
# ============================================================================

@app.post("/api/tickets/{ticket_id}/status")
async def update_ticket_status(
    ticket_id: str,
    status: str,  # Query parameter: open, assigned, in_progress, resolved, closed
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    # Get the ticket
    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    
    # Validate status
    valid_statuses = ["open", "assigned", "in_progress", "resolved", "closed"]
    if status not in valid_statuses:
        raise HTTPException(status_code=400, detail=f"Invalid status. Must be one of: {valid_statuses}")
    
    # Authorization checks
    if current_user.role == "customer":
        # Customers can only view their own tickets and can't change status
        if ticket.customer_id != current_user.id:
            raise HTTPException(status_code=403, detail="Can only update your own tickets")
        raise HTTPException(status_code=403, detail="Customers cannot change ticket status")
    
    # Support agents can only update tickets assigned to them (unless admin)
    if current_user.role == "support_agent" and ticket.assigned_agent_id != current_user.id:
        raise HTTPException(status_code=403, detail="Can only update tickets assigned to you")
    
    # Store old status for email notification
    old_status = ticket.status
    
    # Update status and timestamps
    ticket.status = status
    ticket.updated_at = datetime.utcnow()
    
    # Set resolution/closure timestamps
    if status == "resolved" and old_status != "resolved":
        ticket.resolved_at = datetime.utcnow()
    elif status == "closed" and old_status != "closed":
        ticket.closed_at = datetime.utcnow()
    elif status in ["open", "assigned", "in_progress"]:
        # Reset resolution/closure if moving back to active status
        ticket.resolved_at = None
        ticket.closed_at = None
    
    db.commit()
    db.refresh(ticket)

    # ✅ EMAIL INTEGRATION: Send status update notification
    try:
        # Get customer details
        customer = db.query(User).filter(User.id == ticket.customer_id).first()
        if customer and customer.email:
            EmailService.send_ticket_status_update(ticket, customer.email, old_status, status)
            print(f"📧 Sent status update notification to: {customer.email}")
            print(f"   Status changed: {old_status} → {status}")
        else:
            print("⚠️ No customer email found for status update notification")
    except Exception as email_error:
        print(f"⚠️ Failed to send status update email: {email_error}")
        # Don't fail the status update if email fails
    
    return {
        "message": f"Ticket status updated from {old_status} to {status}",
        "ticket": ticket
    }

@app.get("/api/tickets/{ticket_id}/status-history")
async def get_ticket_status_history(
    ticket_id: str,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    # This would typically query a separate status_history table
    # For now, we'll return basic info from the ticket
    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    
    # Authorization
    if current_user.role == "customer" and ticket.customer_id != current_user.id:
        raise HTTPException(status_code=403, detail="Can only view your own tickets")
    
    # Mock status history (in a real app, this would be from a history table)
    status_history = [
        {
            "status": "open",
            "timestamp": ticket.created_at.isoformat(),
            "changed_by": "system"
        }
    ]
    
    if ticket.assigned_at:
        status_history.append({
            "status": "assigned",
            "timestamp": ticket.assigned_at.isoformat(),
            "changed_by": "system"
        })
    
    if ticket.resolved_at:
        status_history.append({
            "status": "resolved", 
            "timestamp": ticket.resolved_at.isoformat(),
            "changed_by": ticket.assigned_agent_id or "system"
        })
    
    if ticket.closed_at:
        status_history.append({
            "status": "closed",
            "timestamp": ticket.closed_at.isoformat(), 
            "changed_by": ticket.assigned_agent_id or "system"
        })
    
    return {
        "ticket_id": ticket_id,
        "current_status": ticket.status,
        "history": status_history
    }

# Update Support Agent Stats to include new status counts
@app.get("/api/dashboard/support-agent/stats")
async def get_support_agent_dashboard_stats(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    if current_user.role not in ["support_agent", "admin"]:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    # All tickets for support agents to see
    all_tickets = db.query(Ticket).all()
    assigned_tickets = db.query(Ticket).filter(Ticket.assigned_agent_id == current_user.id).all()
    unassigned_tickets = db.query(Ticket).filter(Ticket.assigned_agent_id == None).all()
    
    # Calculate stats
    today = datetime.utcnow().date()
    resolved_today = len([t for t in assigned_tickets if t.status == "resolved" and t.updated_at.date() == today])
    
    stats = {
        "total_tickets": len(all_tickets),
        "assigned_tickets": len(assigned_tickets),
        "unassigned_tickets": len(unassigned_tickets),
        "resolved_today": resolved_today,
        "avg_response_time": 45,
        "high_urgency_tickets": len([t for t in all_tickets if t.urgency >= 4]),
        "open_tickets": len([t for t in all_tickets if t.status == "open"]),
        "my_assigned_tickets": len(assigned_tickets),
        "in_progress_tickets": len([t for t in all_tickets if t.status == "in_progress"]),
        "resolved_tickets": len([t for t in all_tickets if t.status == "resolved"]),
        "closed_tickets": len([t for t in all_tickets if t.status == "closed"])
    }
    
    return stats

@app.get("/cors-test")
async def cors_test():
    return {"message": "CORS test successful", "cors_enabled": True}

@app.get("/test-simple")
async def test_simple():
    return {"status": "ok", "message": "Backend is working"}