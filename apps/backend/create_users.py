# create_users.py
import sys
sys.path.append('.')
from app.models.database import User, engine, Base
from sqlalchemy.orm import Session
from app.core.auth import get_password_hash
import uuid
from sqlalchemy import text

print('🚀 CREATING TEST USERS')
print('=' * 40)

try:
    # Ensure tables exist
    Base.metadata.create_all(bind=engine)
    print('✅ Tables verified')
    
    with Session(engine) as session:
        # Create users
        users_data = [
            {'email': 'customer@test.com', 'password': 'customer123', 'name': 'John Customer', 'role': 'customer'},
            {'email': 'agent@test.com', 'password': 'agent123', 'name': 'Sarah Agent', 'role': 'support_agent'},
            {'email': 'admin@test.com', 'password': 'admin123', 'name': 'Mike Admin', 'role': 'admin'},
        ]
        
        for user_data in users_data:
            user_id = str(uuid.uuid4())
            user = User(
                id=user_id,
                email=user_data['email'],
                full_name=user_data['name'],
                hashed_password=get_password_hash(user_data['password']),
                role=user_data['role']
            )
            session.add(user)
            print('✅ Created: ' + user_data['email'])
        
        session.commit()
        print('✅ All users saved to database')
        
        # Verify
        users = session.query(User).all()
        print('📊 Users in database: ' + str(len(users)))
        for user in users:
            print('   - ' + user.email + ' (' + user.role + ')')
            
except Exception as e:
    print('❌ Error: ' + str(e))
    import traceback
    traceback.print_exc()

print('')
print('🎯 LOGIN CREDENTIALS:')
print('=' * 30)
print('CUSTOMER: customer@test.com / customer123')
print('AGENT:    agent@test.com / agent123')
print('ADMIN:    admin@test.com / admin123')
