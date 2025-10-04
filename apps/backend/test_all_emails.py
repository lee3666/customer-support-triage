# test_all_emails.py
import requests
import sys
sys.path.append(".")
from app.models.database import User, engine, Base
from sqlalchemy.orm import Session
import uuid

print("🚀 TESTING ALL EMAIL INTEGRATIONS")
print("=" * 50)

# Step 1: Ensure we have users
print("1. Ensuring test users exist...")
Base.metadata.create_all(bind=engine)

with Session(engine) as session:
    # Create users if they don't exist
    users_data = [
        {"email": "customer@test.com", "password": "customer123", "name": "John Customer", "role": "customer"},
        {"email": "agent@test.com", "password": "agent123", "name": "Sarah Agent", "role": "support_agent"},
        {"email": "admin@test.com", "password": "admin123", "name": "Mike Admin", "role": "admin"},
    ]
    
    for user_data in users_data:
        existing_user = session.query(User).filter(User.email == user_data["email"]).first()
        if not existing_user:
            user_id = str(uuid.uuid4())
            from app.core.auth import get_password_hash
            user = User(
                id=user_id,
                email=user_data["email"],
                full_name=user_data["name"],
                hashed_password=get_password_hash(user_data["password"]),
                role=user_data["role"]
            )
            session.add(user)
            print(f"   ✅ Created: {user_data['email']}")
        else:
            print(f"   ✅ Found: {user_data['email']}")
    
    session.commit()

# Step 2: Login as customer to create ticket
print("2. Creating test ticket as customer...")
customer_login = requests.post("http://localhost:8001/auth/login", json={
    "email": "customer@test.com",
    "password": "customer123"
})

if customer_login.status_code != 200:
    print("❌ Customer login failed")
    exit()

customer_token = customer_login.json()["access_token"]
customer_headers = {"Authorization": "Bearer " + customer_token}

# Get customer ID
with Session(engine) as session:
    customer = session.query(User).filter(User.email == "customer@test.com").first()
    customer_id = customer.id

# Create ticket
ticket_response = requests.post("http://localhost:8001/api/tickets", json={
    "customer_id": customer_id,
    "subject": "Complete Email Integration Test",
    "description": "Testing all email types: creation, assignment, and status updates"
}, headers=customer_headers)

if ticket_response.status_code != 200:
    print("❌ Ticket creation failed:", ticket_response.text)
    exit()

ticket = ticket_response.json()
ticket_id = ticket["id"]
print("   ✅ Ticket created - check server console for NEW TICKET email")

# Step 3: Login as admin to assign and update status
print("3. Logging in as admin for assignment and status updates...")
admin_login = requests.post("http://localhost:8001/auth/login", json={
    "email": "admin@test.com",
    "password": "admin123"
})

if admin_login.status_code != 200:
    print("❌ Admin login failed")
    exit()

admin_token = admin_login.json()["access_token"]
admin_headers = {"Authorization": "Bearer " + admin_token}

# Step 4: Assign ticket (should trigger assignment email)
print("4. Assigning ticket...")
assign_response = requests.post(f"http://localhost:8001/api/tickets/{ticket_id}/assign", headers=admin_headers)

if assign_response.status_code == 200:
    print("   ✅ Ticket assigned - check server console for ASSIGNMENT email")
else:
    print("   ❌ Assignment failed:", assign_response.text)

# Step 5: Update to in_progress (should trigger status email)
print("5. Updating status to in_progress...")
status_response1 = requests.post(f"http://localhost:8001/api/tickets/{ticket_id}/status?status=in_progress", headers=admin_headers)

if status_response1.status_code == 200:
    print("   ✅ Status updated to in_progress - check server console for STATUS UPDATE email")
else:
    print("   ❌ Status update failed:", status_response1.text)

# Step 6: Update to resolved (should trigger resolution email)
print("6. Updating status to resolved...")
status_response2 = requests.post(f"http://localhost:8001/api/tickets/{ticket_id}/status?status=resolved", headers=admin_headers)

if status_response2.status_code == 200:
    print("   ✅ Status updated to resolved - check server console for RESOLUTION email")
else:
    print("   ❌ Status update failed:", status_response2.text)

print("")
print("🎉 TEST COMPLETE!")
print("=" * 30)
print("📧 Check your SERVER CONSOLE for these emails:")
print("   1. 📧 NEW TICKET notification")
print("   2. 📧 ASSIGNMENT notification") 
print("   3. 📧 STATUS UPDATE (in_progress)")
print("   4. 📧 STATUS UPDATE (resolved)")
print("")
print("If you see all 4, your email integration is 100% complete! 🚀")
