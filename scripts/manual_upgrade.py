"""
Manually run database migrations
Use this if auto-migration fails
"""
import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add the parent directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def manual_upgrade():
    """Manually upgrade database"""
    try:
        # Import after setting up the path
        from api.index import app, db
        from flask_migrate import upgrade, current, heads
        
        with app.app_context():
            print("🔧 Manual Database Migration")
            print("=" * 40)
            
            # Check current status
            try:
                current_rev = current()
                latest_rev = heads()
                print(f"Current revision: {current_rev or 'None'}")
                print(f"Latest revision:  {latest_rev or 'None'}")
            except Exception as e:
                print(f"Status check error: {e}")
            
            # Confirm upgrade
            if current_rev == latest_rev:
                print("✅ Database is already up to date!")
                return True
            
            print("\n⚠️ This will upgrade your database schema.")
            confirm = input("Continue? (y/N): ").strip().lower()
            
            if confirm != 'y':
                print("❌ Migration cancelled")
                return False
            
            # Run upgrade
            print("\n🚀 Running database upgrade...")
            try:
                upgrade()
                print("✅ Database upgrade completed successfully!")
                
                # Verify upgrade
                new_current = current()
                print(f"New current revision: {new_current}")
                
                return True
                
            except Exception as e:
                print(f"❌ Migration failed: {e}")
                print("\n🔧 Troubleshooting:")
                print("  1. Check database connection")
                print("  2. Verify migration files")
                print("  3. Check for schema conflicts")
                print("  4. Consider rollback if needed")
                return False
            
    except Exception as e:
        print(f"❌ Error during manual upgrade: {e}")
        return False

if __name__ == "__main__":
    success = manual_upgrade()
    if not success:
        sys.exit(1)
