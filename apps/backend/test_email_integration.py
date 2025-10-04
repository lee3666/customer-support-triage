# test_email_integration.py
import requests
import sys
sys.path.append(".")
from app.models.database import User, engine
from sqlalchemy.orm import Session

print("🚀 TESTING EMAIL INTEGRATION")
print("=" * 40)

# Get customer ID from database
with Session(engine) as session:
    user = session.query(User).filter(User.email == "customer@test.com").first()
    if user:
        customer_id = user.id
        print("Found customer: " + user.email)
        print("Customer ID: " + customer_id)
    else:
        print("❌ Customer not found")
        exit()

# Login
print("1. Logging in...")
login_response = requests.post("http://localhost:8001/auth/login", json={
    "email": "customer@test.com",
    "password": "customer123"
})

if login_response.status_code == 200:
    token = login_response.json()["access_token"]
    headers = {"Authorization": "Bearer " + token}
    print("✅ Login successful")
    
    # Create ticket
    print("2. Creating ticket...")
    ticket_data = {
        "customer_id": customer_id,
        "subject": "Email Integration Test on Port 8001",
        "description": "Testing if emails are sent when creating tickets via the frontend port."
    }
    
    ticket_response = requests.post("http://localhost:8001/api/tickets", json=ticket_data, headers=headers)
    
    if ticket_response.status_code == 200:
        print("✅ Ticket created successfully!")
        print("3. 📧 CHECK YOUR SERVER CONSOLE!")
        print("   Look for: 📧 Sent new ticket notification to: customer@test.com")
        print("")
        print("🎉 If you see that, everything is working!")
    else:
        print("❌ Ticket creation failed:")
        print("   Status: " + str(ticket_response.status_code))
        print("   Error: " + ticket_response.text)
else:
    print("❌ Login failed:")
    print("   Status: " + str(login_response.status_code))
    print("   Error: " + login_response.text)
