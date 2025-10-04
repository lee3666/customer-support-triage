# test_login.py
import requests
import json

print("🔐 TESTING LOGIN ON PORT 8001")
print("=" * 40)

users = [
    {"email": "customer@test.com", "password": "customer123", "role": "Customer"},
    {"email": "agent@test.com", "password": "agent123", "role": "Agent"},
    {"email": "admin@test.com", "password": "admin123", "role": "Admin"},
]

for user in users:
    print("Testing: " + user["email"])
    try:
        response = requests.post("http://localhost:8001/auth/login", json={
            "email": user["email"],
            "password": user["password"]
        })
        
        if response.status_code == 200:
            print("✅ LOGIN SUCCESS")
            token_data = response.json()
            print("   Token: " + token_data["access_token"][:30] + "...")
        else:
            print("❌ LOGIN FAILED")
            print("   Status: " + str(response.status_code))
            print("   Error: " + response.text)
            
    except Exception as e:
        print("❌ REQUEST ERROR: " + str(e))
    
    print("---")
