# debug_database.py
import sys
sys.path.append('.')
from app.models.database import engine, User, Base
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.core.auth import get_password_hash
import uuid

def check_database():
    print('🔧 DATABASE DEBUGGING')
    print('=' * 40)
    
    try:
        # Test connection
        with engine.connect() as conn:
            result = conn.execute(text('SELECT 1'))
            print('✅ Database connection successful')
        
        # List tables
        with engine.connect() as conn:
            tables = conn.execute(text("SELECT name FROM sqlite_master WHERE type='table'")).fetchall()
            print('Tables in database:')
            for table in tables:
                print(f'  - {table[0]}')
            
            # Check users table
            users_table = conn.execute(text("SELECT name FROM sqlite_master WHERE type='table' AND name='users'")).fetchone()
            if users_table:
                print('✅ Users table exists')
                # Show columns
                columns = conn.execute(text('PRAGMA table_info(users)')).fetchall()
                print('Users table columns:')
                for col in columns:
                    print(f'  - {col[1]} ({col[2]})')
            else:
                print('❌ Users table does not exist')
                
    except Exception as e:
        print(f'❌ Database error: {e}')
        return False
    
    return True

def create_tables():
    print('\n🔄 CREATING TABLES')
    print('=' * 30)
    try:
        Base.metadata.create_all(bind=engine)
        print('✅ Tables created successfully')
        return True
    except Exception as e:
        print(f'❌ Table creation failed: {e}')
        return False

def create_users():
    print('\n👥 CREATING TEST USERS')
    print('=' * 30)
    
    try:
        with Session(engine) as session:
            users_to_create = [
                ('customer@test.com', 'customer123', 'John Customer', 'customer'),
                ('agent@test.com', 'agent123', 'Sarah Agent', 'support_agent'), 
                ('admin@test.com', 'admin123', 'Mike Admin', 'admin')
            ]
            
            for email, password, name, role in users_to_create:
                user = User(
                    id=str(uuid.uuid4()),
                    email=email,
                    full_name=name,
                    hashed_password=get_password_hash(password),
                    role=role
                )
                session.add(user)
                print(f'✅ Added: {email}')
            
            session.commit()
            print('✅ All users committed to database')
            
            # Verify
            users = session.query(User).all()
            print(f'Total users in database: {len(users)}')
            for user in users:
                print(f'  - {user.email} ({user.role}) - ID: {user.id}')
            
            return True
            
    except Exception as e:
        print(f'❌ User creation failed: {e}')
        import traceback
        print('Traceback:')
        print(traceback.format_exc())
        return False

if __name__ == '__main__':
    # Step 1: Check database
    if check_database():
        # Step 2: Create tables if needed
        with engine.connect() as conn:
            users_table = conn.execute(text("SELECT name FROM sqlite_master WHERE type='table' AND name='users'")).fetchone()
            if not users_table:
                create_tables()
        
        # Step 3: Create users
        create_users()
