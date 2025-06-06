"""
Backup and restore PostgreSQL database
"""
import os
import sys
import subprocess
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def get_db_config():
    """Get database configuration from environment"""
    database_url = os.getenv('DATABASE_URL')
    if not database_url:
        print("❌ DATABASE_URL environment variable not found")
        return None
    
    # Parse DATABASE_URL
    # Format: postgresql://user:password@host:port/database
    try:
        from urllib.parse import urlparse
        parsed = urlparse(database_url)
        
        return {
            'host': parsed.hostname,
            'port': parsed.port or 5432,
            'database': parsed.path[1:],  # Remove leading slash
            'username': parsed.username,
            'password': parsed.password
        }
    except Exception as e:
        print(f"❌ Error parsing DATABASE_URL: {e}")
        return None

def backup_database(output_file=None):
    """Create a database backup"""
    try:
        db_config = get_db_config()
        if not db_config:
            return False
        
        # Generate backup filename if not provided
        if not output_file:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_file = f"backup_{db_config['database']}_{timestamp}.sql"
        
        print(f"📦 Creating database backup...")
        print(f"Database: {db_config['database']}")
        print(f"Output file: {output_file}")
        
        # Set environment variable for password
        env = os.environ.copy()
        env['PGPASSWORD'] = db_config['password']
        
        # Build pg_dump command
        cmd = [
            'pg_dump',
            '-h', db_config['host'],
            '-p', str(db_config['port']),
            '-U', db_config['username'],
            '-d', db_config['database'],
            '--no-password',
            '--verbose',
            '--clean',
            '--if-exists',
            '--create',
            '-f', output_file
        ]
        
        # Run backup
        result = subprocess.run(cmd, env=env, capture_output=True, text=True)
        
        if result.returncode == 0:
            # Get file size
            file_size = os.path.getsize(output_file)
            size_mb = file_size / (1024 * 1024)
            
            print(f"✅ Backup created successfully!")
            print(f"📄 File: {output_file}")
            print(f"📊 Size: {size_mb:.2f} MB")
            return True
        else:
            print(f"❌ Backup failed!")
            print(f"Error: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Error creating backup: {e}")
        return False

def restore_database(backup_file):
    """Restore database from backup"""
    try:
        if not os.path.exists(backup_file):
            print(f"❌ Backup file not found: {backup_file}")
            return False
        
        db_config = get_db_config()
        if not db_config:
            return False
        
        print(f"🔄 Restoring database from backup...")
        print(f"Backup file: {backup_file}")
        print(f"Target database: {db_config['database']}")
        
        # Warning
        print("\n⚠️ WARNING: This will overwrite the current database!")
        confirm = input("Continue? (y/N): ").strip().lower()
        
        if confirm != 'y':
            print("❌ Restore cancelled")
            return False
        
        # Set environment variable for password
        env = os.environ.copy()
        env['PGPASSWORD'] = db_config['password']
        
        # Build psql command
        cmd = [
            'psql',
            '-h', db_config['host'],
            '-p', str(db_config['port']),
            '-U', db_config['username'],
            '-d', 'postgres',  # Connect to postgres db first
            '--no-password',
            '-f', backup_file
        ]
        
        # Run restore
        result = subprocess.run(cmd, env=env, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Database restored successfully!")
            return True
        else:
            print(f"❌ Restore failed!")
            print(f"Error: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Error restoring database: {e}")
        return False

def main():
    """Main function"""
    if len(sys.argv) < 2:
        print("📦 Database Backup & Restore Tool")
        print("=" * 40)
        print("Usage:")
        print("  python scripts/backup_database.py backup [filename]")
        print("  python scripts/backup_database.py restore <filename>")
        print("\nExamples:")
        print("  python scripts/backup_database.py backup")
        print("  python scripts/backup_database.py backup my_backup.sql")
        print("  python scripts/backup_database.py restore backup_20231201_120000.sql")
        return
    
    action = sys.argv[1].lower()
    
    if action == 'backup':
        output_file = sys.argv[2] if len(sys.argv) > 2 else None
        success = backup_database(output_file)
    elif action == 'restore':
        if len(sys.argv) < 3:
            print("❌ Backup file is required for restore")
            return
        backup_file = sys.argv[2]
        success = restore_database(backup_file)
    else:
        print(f"❌ Unknown action: {action}")
        print("Available actions: backup, restore")
        return
    
    if not success:
        sys.exit(1)

if __name__ == "__main__":
    main()
