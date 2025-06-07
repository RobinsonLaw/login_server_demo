import os
from urllib.parse import urlparse

def parse_and_set_db_vars():
    # Check for both DATABASE_URL and POSTGRES_URL
    database_url = os.getenv('DATABASE_URL') or os.getenv('POSTGRES_URL')
    
    if not database_url:
        print("❌ Neither DATABASE_URL nor POSTGRES_URL found in environment")
        print("Current environment variables:")
        for key in os.environ:
            if 'postgres' in key.lower() or 'database' in key.lower():
                print(f"  {key}: {os.environ[key][:30]}...")
        return False
    
    print(f"Found DATABASE_URL: {database_url[:50]}...")
    
    # Parse the URL
    try:
        parsed = urlparse(database_url)
        
        # Extract components
        db_user = parsed.username or 'postgres'
        db_password = parsed.password or 'password'
        db_host = parsed.hostname or 'localhost'
        db_port = str(parsed.port or 5432)
        db_name = parsed.path[1:] if parsed.path else 'flask_app'  # Remove leading '/'
        
        print("\n=== Parsed Database Connection Details ===")
        print(f"DB_USER: {db_user}")
        print(f"DB_HOST: {db_host}")
        print(f"DB_PORT: {db_port}")
        print(f"DB_NAME: {db_name}")
        print(f"DB_PASSWORD: {'*' * len(db_password)}")
        
        # Set environment variables for this session
        os.environ['DB_USER'] = db_user
        os.environ['DB_PASSWORD'] = db_password
        os.environ['DB_HOST'] = db_host
        os.environ['DB_PORT'] = db_port
        os.environ['DB_NAME'] = db_name
        
        print("\n✅ Environment variables set successfully!")
        
        # Generate export commands for manual use
        print("\n=== Manual Export Commands ===")
        print(f'export DB_USER="{db_user}"')
        print(f'export DB_PASSWORD="{db_password}"')
        print(f'export DB_HOST="{db_host}"')
        print(f'export DB_PORT="{db_port}"')
        print(f'export DB_NAME="{db_name}"')
        
        return True
        
    except Exception as e:
        print(f"❌ Error parsing DATABASE_URL: {e}")
        return False

if __name__ == "__main__":
    parse_and_set_db_vars()