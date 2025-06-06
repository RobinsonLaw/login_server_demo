"""
Initialize Flask-Migrate for the project
Run this script once to set up migrations
"""
import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add the parent directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def init_migrations():
    """Initialize Flask-Migrate"""
    try:
        # Import after setting up the path
        from api.index import app, db
        from flask_migrate import init, migrate, upgrade
        
        with app.app_context():
            print("🔧 Initializing Flask-Migrate...")
            
            # Initialize migrations directory
            try:
                init()
                print("✅ Migrations directory created")
            except Exception as e:
                if "already exists" in str(e).lower():
                    print("📁 Migrations directory already exists")
                else:
                    raise e
            
            # Create initial migration
            print("📝 Creating initial migration...")
            try:
                migrate(message="Initial migration")
                print("✅ Initial migration created")
            except Exception as e:
                print(f"⚠️ Migration creation warning: {e}")
            
            # Apply migration
            print("🚀 Applying initial migration...")
            try:
                upgrade()
                print("✅ Initial migration applied successfully")
            except Exception as e:
                print(f"⚠️ Migration application warning: {e}")
            
            print("\n🎉 Flask-Migrate initialization completed!")
            print("📋 Next steps:")
            print("  1. Modify your models in api/index.py")
            print("  2. Run: python scripts/create_migration.py 'Description of changes'")
            print("  3. Deploy - auto-migration will handle the rest!")
            
    except Exception as e:
        print(f"❌ Error initializing migrations: {e}")
        return False
    
    return True

if __name__ == "__main__":
    success = init_migrations()
    if not success:
        sys.exit(1)
