# create_users_fixed.py
import sys
sys.path.append('.')
from app.models.database import User, engine, Base
from sqlalchemy.orm import Session
from app.core.auth import get_password_hash
import uuid
from sqlalchemy import text

def ensure_tables_exist():
    """Make sure tables are created"""
    print('🔄 Ensuring tables exist...')
    try:
        Base.metadata.create_all(bind=engine)
        print('✅ Tables verified')
        return True
    except Exception as e:
        print(f'❌ Table creation failed: {e}')
        return False

def create_users():
    """Create test users"""
    print('👥 Creating test users...')
    
    with Session(engine) as session:
        # First, verify we can query the database
        try:
            test_query = session.execute(text('SELECT 1'))
            print('✅ Database query successful')
        except Exception as e:
            print(f'❌ Database query failed: {e}')
            return False
        
        # Create users
        users_data = [
            {'email': 'customer@test.com', 'password': 'customer123', 'name': 'John Customer', 'role': 'customer'},
            {'email': 'agent@test.com', 'password': 'agent123', 'name': 'Sarah Agent', 'role': 'support_agent'},
            {'email': 'admin@test.com', 'password': 'admin123', 'name': 'Mike Admin', 'role': 'admin'},
        ]
        
        created_count = 0
        for user_data in users_data:
            try:
                user_id = str(uuid.uuid4())
                user = User(
                    id=user_id,
                    email=user_data['email'],
                    full_name=user_data['name'],
                    hashed_password=get_password_hash(user_data['password']),
                    role=user_data['role']
                )
                session.add(user)
                print(f'✅ Added: {user_data["email"]}')
                created_count += 1
            except Exception as e:
                print(f'❌ Failed to create {user_data["email"]}: {e}')
        
        try:
            session.commit()
            print(f'✅ Successfully committed {created_count} users to database')
            
            # Verify users were saved
            saved_users = session.query(User).all()
            print(f'📊 Total users in database: {len(saved_users)}')
            for user in saved_users:
                print(f'   - {user.email} ({user.role})')
                
            return True
        except Exception as e:
            print(f'❌ Commit failed: {e}')
            session.rollback()
            return False

if __name__ == '__main__':
    print('🚀 USER CREATION SCRIPT')
    print('=' * 50)
    
    if ensure_tables_exist():
        create_users()
        
    print('')
    print('🎯 LOGIN CREDENTIALS:')
    print('=' * 40)
    print('CUSTOMER:    customer@test.com / customer123')
    print('SUPPORT:     agent@test.com / agent123')
    print('ADMIN:       admin@test.com / admin123')
