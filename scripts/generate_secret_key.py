import secrets
import os

# Method 1: Generate a random secret key
secret_key = secrets.token_hex(32)
print(f"Generated SECRET_KEY: {secret_key}")

# Method 2: Using os.urandom (alternative)
secret_key_alt = os.urandom(32).hex()
print(f"Alternative SECRET_KEY: {secret_key_alt}")

# Method 3: Using Python's built-in uuid
import uuid
secret_key_uuid = str(uuid.uuid4()).replace('-', '')
print(f"UUID-based SECRET_KEY: {secret_key_uuid}")