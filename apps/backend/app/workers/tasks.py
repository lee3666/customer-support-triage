from .celery import celery_app
from app.services.ai_service import ai_service
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

logger = logging.getLogger(__name__)

# Database setup for workers
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:pass@localhost:5432/support")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@celery_app.task(bind=True, max_retries=3)
def process_ticket_ai(self, ticket_id: str):
    """Background task for advanced AI processing"""
    db = SessionLocal()
    try:
        from app.models.database import Ticket
        
        # Get ticket from database
        ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
        if not ticket:
            logger.error(f"Ticket {ticket_id} not found")
            return
        
        # Enhanced AI analysis (can do more complex processing here)
        ai_analysis = ai_service.analyze_ticket(ticket.subject, ticket.description)
        
        # Update ticket with enhanced AI data
        ticket.ai_urgency = ai_analysis['urgency']
        ticket.ai_sentiment = ai_analysis['sentiment']
        ticket.ai_sentiment_score = ai_analysis['sentiment_score']
        ticket.ai_category = ai_analysis['category']
        ticket.ai_confidence = ai_analysis['confidence']
        
        # Additional processing: Calculate response time estimate
        if ai_analysis['urgency'] >= 4:
            ticket.urgency = 4  # Ensure high urgency tickets get priority
            # Trigger immediate email for high urgency
            send_email_notification.delay(
                ticket_id,
                "High Urgency Ticket Created",
                f"High urgency ticket requires immediate attention: {ticket.subject}"
            )
        
        db.commit()
        logger.info(f"Successfully processed ticket {ticket_id} with AI")
        
    except Exception as exc:
        db.rollback()
        logger.error(f"Failed to process ticket {ticket_id}: {exc}")
        
        if self.request.retries < self.max_retries:
            # Exponential backoff
            retry_delay = 2 ** self.request.retries
            raise self.retry(countdown=retry_delay, exc=exc)
    finally:
        db.close()

@celery_app.task(bind=True, max_retries=3)
def send_email_notification(self, ticket_id: str, subject: str, message: str):
    """Background task for sending email notifications"""
    try:
        # For demo purposes - in production, use real SMTP credentials
        logger.info(f"EMAIL Notification: {subject}")
        logger.info(f"Ticket: {ticket_id}")
        logger.info(f"Message: {message}")
        logger.info("--- Email would be sent in production ---")
        
        # Example of real email sending (commented out for demo):
        """
        msg = MIMEMultipart()
        msg['From'] = 'support@yourcompany.com'
        msg['To'] = 'agents@yourcompany.com'
        msg['Subject'] = subject
        
        body = f\"\"\"
        New Support Ticket Notification
        
        Ticket ID: {ticket_id}
        {message}
        
        Please review in the support system.
        \"\"\"
        msg.attach(MIMEText(body, 'plain'))
        
        with smtplib.SMTP('smtp.yourcompany.com', 587) as server:
            server.starttls()
            server.login('username', 'password')
            server.send_message(msg)
        """
        
        logger.info("SUCCESS: Email notification processed successfully")
        
    except Exception as exc:
        logger.error(f"Failed to send email: {exc}")
        
        if self.request.retries < self.max_retries:
            retry_delay = 2 ** self.request.retries
            raise self.retry(countdown=retry_delay, exc=exc)

@celery_app.task
def send_welcome_email(customer_email: str, customer_name: str):
    """Send welcome email to new customers"""
    try:
        logger.info(f"Welcome email would be sent to: {customer_email}")
        logger.info(f"Hello {customer_name}, thank you for contacting support!")
        logger.info("We'll get back to you shortly.")
        
    except Exception as exc:
        logger.error(f"Failed to send welcome email: {exc}")