import requests

print('🔐 TESTING NEW LOGIN CREDENTIALS')
print('=' * 35)

users = [
    {'email': 'test@customer.com', 'password': 'test123', 'role': 'Customer'},
    {'email': 'test@agent.com', 'password': 'test123', 'role': 'Agent'},
    {'email': 'test@admin.com', 'password': 'test123', 'role': 'Admin'},
]

for user in users:
    print(f'Testing {user["role"]}...')
    try:
        response = requests.post('http://localhost:8001/auth/login', json={
            'email': user['email'],
            'password': user['password']
        })
        
        if response.status_code == 200:
            print(f'✅ {user["role"]} LOGIN SUCCESS!')
            token = response.json()['access_token'][:30] + '...'
            print(f'   Token: {token}')
        else:
            print(f'❌ {user["role"]} LOGIN FAILED')
            print(f'   Error: {response.text}')
    except Exception as e:
        print(f'❌ Request failed: {e}')
    print('---')