# test_integration.py
import os
import sys
from datetime import datetime

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.services.email_service import EmailService

# Mock classes that match YOUR actual model structure
class MockTicket:
    def __init__(self, ticket_id, subject, description, urgency, status="open", customer_id=""):
        self.id = ticket_id
        self.subject = subject
        self.description = description
        self.urgency = urgency
        self.status = status
        self.customer_id = customer_id  # Note: customer_id instead of customer_email

class MockAgent:
    def __init__(self, agent_id, full_name, email):
        self.id = agent_id
        self.full_name = full_name
        self.email = email

def test_all_email_types():
    print("Testing all email types...")
    
    # Create mock data
    ticket = MockTicket(
        ticket_id="TKT-12345-ABCD",
        subject="Website not loading properly",
        description="When I visit our homepage, it shows a 500 error. This started about 2 hours ago.",
        urgency=4,
        customer_id="CUST-001"
    )
    
    agent = MockAgent(
        agent_id="AGENT-001",
        full_name="John Smith",
        email="john.smith@support.com"
    )
    
    # Test 1: New ticket notification - NOTE: We need to pass email separately since it's not in Ticket model
    print("\n1. Testing new ticket notification...")
    customer_email = "customer@example.com"  # You'll get this from the User table using customer_id
    success1 = EmailService.send_new_ticket_notification(ticket, customer_email)
    print(f"   Result: {'✅ Success' if success1 else '❌ Failed'}")
    
    # Test 2: Ticket assigned notification
    print("\n2. Testing ticket assigned notification...")
    success2 = EmailService.send_ticket_assigned_notification(ticket, agent, customer_email)
    print(f"   Result: {'✅ Success' if success2 else '❌ Failed'}")
    
    # Test 3: Status update notification
    print("\n3. Testing status update notification...")
    success3 = EmailService.send_ticket_status_update(ticket, customer_email, "open", "in_progress")
    print(f"   Result: {'✅ Success' if success3 else '❌ Failed'}")
    
    print(f"\n📊 Summary: {sum([success1, success2, success3])}/3 emails sent successfully")
    return all([success1, success2, success3])

if __name__ == "__main__":
    print("🚀 Testing Email Service Integration")
    print("=" * 50)
    test_all_email_types()
