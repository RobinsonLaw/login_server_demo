"""
Rollback database migration
Use with caution - may cause data loss
"""
import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add the parent directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def rollback_migration(target_revision=None):
    """Rollback to a specific migration"""
    try:
        # Import after setting up the path
        from api.index import app
        from flask_migrate import downgrade, current, history
        
        with app.app_context():
            print("⚠️ Database Migration Rollback")
            print("=" * 40)
            print("🚨 WARNING: This may cause data loss!")
            
            # Show current status
            try:
                current_rev = current()
                print(f"Current revision: {current_rev or 'None'}")
            except Exception as e:
                print(f"Status check error: {e}")
                return False
            
            # Get target revision
            if not target_revision:
                if len(sys.argv) > 1:
                    target_revision = sys.argv[1]
                else:
                    print("\nAvailable options:")
                    print("  - 'prev' or '-1' for previous revision")
                    print("  - Specific revision ID")
                    print("  - 'base' for initial state")
                    target_revision = input("Enter target revision: ").strip()
            
            if not target_revision:
                print("❌ Target revision is required")
                return False
            
            # Convert 'prev' to -1
            if target_revision.lower() == 'prev':
                target_revision = '-1'
            
            # Multiple confirmations for safety
            print(f"\n🎯 Target revision: {target_revision}")
            print("⚠️ This will rollback your database schema.")
            print("💾 Make sure you have a backup!")
            
            confirm1 = input("Are you sure? (y/N): ").strip().lower()
            if confirm1 != 'y':
                print("❌ Rollback cancelled")
                return False
            
            confirm2 = input("This may cause DATA LOSS. Continue? (y/N): ").strip().lower()
            if confirm2 != 'y':
                print("❌ Rollback cancelled")
                return False
            
            # Run rollback
            print(f"\n🔄 Rolling back to revision: {target_revision}")
            try:
                downgrade(target_revision)
                print("✅ Rollback completed successfully!")
                
                # Verify rollback
                new_current = current()
                print(f"New current revision: {new_current}")
                
                print("\n📋 Next steps:")
                print("  1. Verify your application works correctly")
                print("  2. Check for any data inconsistencies")
                print("  3. Consider creating a new migration if needed")
                
                return True
                
            except Exception as e:
                print(f"❌ Rollback failed: {e}")
                print("\n🔧 Recovery options:")
                print("  1. Restore from backup")
                print("  2. Try manual database repair")
                print("  3. Contact support if needed")
                return False
            
    except Exception as e:
        print(f"❌ Error during rollback: {e}")
        return False

if __name__ == "__main__":
    success = rollback_migration()
    if not success:
        sys.exit(1)
