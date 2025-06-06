"""
Check migration status and database information
"""
import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add the parent directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def check_migration_status():
    """Check current migration status"""
    try:
        # Import after setting up the path
        from api.index import app, db
        from flask_migrate import current, heads
        
        with app.app_context():
            print("📊 Migration Status Report")
            print("=" * 50)
            
            # Get current revision
            try:
                current_rev = current()
                print(f"Current revision: {current_rev or 'None'}")
            except Exception as e:
                print(f"Current revision: Error - {e}")
            
            # Get latest revision
            try:
                latest_rev = heads()
                print(f"Latest revision:  {latest_rev or 'None'}")
            except Exception as e:
                print(f"Latest revision:  Error - {e}")
            
            # Check if up to date
            try:
                if current_rev == latest_rev:
                    print("Status: ✅ Database is up to date")
                else:
                    print("Status: ⚠️ Database needs migration")
            except:
                print("Status: ❓ Unable to determine")
            
            print("\n📋 Database Tables:")
            print("-" * 30)
            
            # List tables
            try:
                inspector = db.inspect(db.engine)
                tables = inspector.get_table_names()
                
                if tables:
                    for table in sorted(tables):
                        columns = inspector.get_columns(table)
                        print(f"📄 {table} ({len(columns)} columns)")
                        for col in columns[:3]:  # Show first 3 columns
                            print(f"   - {col['name']} ({col['type']})")
                        if len(columns) > 3:
                            print(f"   ... and {len(columns) - 3} more")
                else:
                    print("No tables found")
                    
            except Exception as e:
                print(f"Error listing tables: {e}")
            
            # Migration files
            print("\n📁 Migration Files:")
            print("-" * 30)
            
            migrations_dir = os.path.join(os.path.dirname(__file__), '..', 'migrations', 'versions')
            if os.path.exists(migrations_dir):
                migration_files = [f for f in os.listdir(migrations_dir) if f.endswith('.py')]
                if migration_files:
                    for i, file in enumerate(sorted(migration_files)[-5:], 1):  # Show last 5
                        print(f"{i}. {file}")
                    if len(migration_files) > 5:
                        print(f"... and {len(migration_files) - 5} more")
                else:
                    print("No migration files found")
            else:
                print("Migrations directory not found")
            
    except Exception as e:
        print(f"❌ Error checking migration status: {e}")
        return False
    
    return True

if __name__ == "__main__":
    check_migration_status()
