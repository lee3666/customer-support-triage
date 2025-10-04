# complete_test.py
import sys
sys.path.append(".")
from app.models.database import User, engine, Base
from sqlalchemy.orm import Session
from app.core.auth import get_password_hash
import uuid
import requests

print("🚀 COMPLETE SYSTEM TEST")
print("=" * 50)

# Step 1: Create tables and users
print("1. Creating tables and users...")
Base.metadata.create_all(bind=engine)

with Session(engine) as session:
    users_data = [
        {"email": "customer@test.com", "password": "customer123", "name": "John Customer", "role": "customer"},
        {"email": "agent@test.com", "password": "agent123", "name": "Sarah Agent", "role": "support_agent"},
        {"email": "admin@test.com", "password": "admin123", "name": "Mike Admin", "role": "admin"},
    ]
    
    for user_data in users_data:
        user_id = str(uuid.uuid4())
        user = User(
            id=user_id,
            email=user_data["email"],
            full_name=user_data["name"],
            hashed_password=get_password_hash(user_data["password"]),
            role=user_data["role"]
        )
        session.add(user)
        print("   ✅ Created: " + user_data["email"])
    
    session.commit()
    
    # Get customer ID for email test
    customer = session.query(User).filter(User.email == "customer@test.com").first()
    customer_id = customer.id

print("2. Testing login...")
login_response = requests.post("http://localhost:8001/auth/login", json={
    "email": "customer@test.com",
    "password": "customer123"
})

if login_response.status_code == 200:
    token = login_response.json()["access_token"]
    headers = {"Authorization": "Bearer " + token}
    print("   ✅ Login successful")
    
    print("3. Testing email integration...")
    ticket_data = {
        "customer_id": customer_id,
        "subject": "Complete System Test",
        "description": "Testing the entire system workflow including email notifications."
    }
    
    ticket_response = requests.post("http://localhost:8001/api/tickets", json=ticket_data, headers=headers)
    
    if ticket_response.status_code == 200:
        print("   ✅ Ticket created successfully!")
        print("")
        print("🎉 SYSTEM READY!")
        print("=" * 30)
        print("📧 Check server console for email confirmation")
        print("💻 Now try logging into your frontend with:")
        print("   Email: customer@test.com")
        print("   Password: customer123")
    else:
        print("   ❌ Ticket creation failed")
else:
    print("   ❌ Login failed")
