import os
import sys
from flask_migrate import Migrate, init as migrate_init, migrate as create_migration

# Add the parent directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import your Flask app and db
from app import app, db  # Adjust based on your actual app structure

def initialize_migrations():
    # Get database URL from environment
    database_url = os.environ.get('POSTGRES_URL') or os.environ.get('DATABASE_URL')
    
    if not database_url:
        raise ValueError("No database URL found in environment variables")
    
    # Fix the dialect name - change postgres:// to postgresql://
    if database_url.startswith('postgres://'):
        database_url = database_url.replace('postgres://', 'postgresql://', 1)
        print("Fixed database URL: changed 'postgres://' to 'postgresql://'")
    
    # Set the database URI in Flask config
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
    print(f"Using database URI with dialect: {database_url.split('://')[0]}")
    
    # Initialize Flask-Migrate (this creates the Migrate object)
    migrate = Migrate(app, db)
    
    with app.app_context():
        try:
            # Initialize migrations folder (creates migrations/ directory)
            migrate_init()
            print("✅ Migrations directory initialized")
            
            # Create initial migration
            create_migration(message="Initial migration")
            print("✅ Initial migration created")
            
        except Exception as e:
            print(f"❌ Error during migration setup: {e}")
            raise
        
        print("🎉 Migrations initialized successfully!")

if __name__ == "__main__":
    initialize_migrations()