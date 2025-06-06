"""
Create a new database migration
Usage: python scripts/create_migration.py "Description of changes"
"""
import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add the parent directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def create_migration(message=None):
    """Create a new migration"""
    try:
        # Get migration message
        if not message:
            if len(sys.argv) > 1:
                message = sys.argv[1]
            else:
                message = input("Enter migration description: ").strip()
        
        if not message:
            print("❌ Migration message is required")
            return False
        
        # Import after setting up the path
        from api.index import app
        from flask_migrate import migrate
        
        with app.app_context():
            print(f"📝 Creating migration: {message}")
            
            # Create migration
            migrate(message=message)
            print("✅ Migration created successfully")
            
            print("\n📋 Next steps:")
            print("  1. Review the generated migration file in migrations/versions/")
            print("  2. Test the migration locally")
            print("  3. Deploy to production (auto-migration will apply it)")
            
    except Exception as e:
        print(f"❌ Error creating migration: {e}")
        return False
    
    return True

if __name__ == "__main__":
    success = create_migration()
    if not success:
        sys.exit(1)
