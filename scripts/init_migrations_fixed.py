import os
import sys
from urllib.parse import urlparse
from flask_migrate import init as migrate_init, migrate as create_migration

# Add the parent directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def setup_db_environment():
    """Parse DATABASE_URL/POSTGRES_URL and set individual DB environment variables"""
    database_url = os.getenv('DATABASE_URL') or os.getenv('POSTGRES_URL')
    
    if database_url:
        print(f"Found database URL: {database_url[:50]}...")
        
        # Fix dialect if needed (postgres:// -> postgresql://)
        if database_url.startswith('postgres://'):
            database_url = database_url.replace('postgres://', 'postgresql://', 1)
            print("✅ Fixed dialect: postgres:// → postgresql://")
        
        parsed = urlparse(database_url)
        
        # Set individual environment variables
        os.environ['DB_USER'] = parsed.username or 'postgres'
        os.environ['DB_PASSWORD'] = parsed.password or 'password'
        os.environ['DB_HOST'] = parsed.hostname or 'localhost'
        os.environ['DB_PORT'] = str(parsed.port or 5432)
        os.environ['DB_NAME'] = parsed.path[1:] if parsed.path else 'flask_app'
        
        print(f"✅ Set DB_HOST to: {os.environ['DB_HOST']}")
        print(f"✅ Set DB_PORT to: {os.environ['DB_PORT']}")
        print(f"✅ Set DB_NAME to: {os.environ['DB_NAME']}")
        print(f"✅ Set DB_USER to: {os.environ['DB_USER']}")
        return True
    else:
        print("❌ No DATABASE_URL or POSTGRES_URL found")
        return False

def initialize_migrations():
    print("=== Migration Initialization ===")
    
    # First, set up the database environment variables
    if not setup_db_environment():
        print("Failed to set up database environment")
        return
    
    # Import your Flask app and db AFTER setting environment variables
    try:
        from app import app, db
        print("✅ Successfully imported app and db")
    except ImportError as e:
        print(f"❌ Error importing app: {e}")
        return
    
    # Show the final database URI (hide password)
    db_uri = app.config['SQLALCHEMY_DATABASE_URI']
    if '@' in db_uri:
        parts = db_uri.split('@')
        safe_uri = parts[0].split(':')[:-1] + ['****@'] + parts[1:]
        print(f"Database URI: {''.join(safe_uri)}")
    else:
        print(f"Database URI: {db_uri}")
    
    with app.app_context():
        try:
            # Test connection first
            print("Testing database connection...")
            connection = db.engine.connect()
            connection.close()
            print("✅ Database connection successful")
            
            # Initialize migrations folder
            migrate_init()
            print("✅ Migrations directory initialized")
            
            # Create initial migration
            create_migration(message="Initial migration")
            print("✅ Initial migration created")
            
        except Exception as e:
            print(f"❌ Error: {e}")
            print("\nTroubleshooting:")
            print("1. Verify your DATABASE_URL is correct")
            print("2. Check if the database server is accessible")
            print("3. Ensure the database exists")
            return
        
        print("🎉 Migrations initialized successfully!")

if __name__ == "__main__":
    initialize_migrations()