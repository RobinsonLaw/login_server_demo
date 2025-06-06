import requests
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Base URL - change this to your Vercel deployment URL
BASE_URL = os.getenv('VERCEL_URL', 'http://localhost:5000')
if not BASE_URL.startswith('http'):
    BASE_URL = f'https://{BASE_URL}'

def test_vercel_api():
    print("🧪 Testing Flask API Server on Vercel")
    print(f"🌐 Base URL: {BASE_URL}")
    print("=" * 60)
    
    # Test 1: Health Check
    print("\n1. Testing Health Check...")
    try:
        response = requests.get(f"{BASE_URL}/api/health", timeout=30)
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    except Exception as e:
        print(f"Error: {e}")
    
    # Test 2: API Root
    print("\n2. Testing API Root...")
    try:
        response = requests.get(f"{BASE_URL}/api", timeout=30)
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    except Exception as e:
        print(f"Error: {e}")
    
    # Test 3: Register User
    print("\n3. Testing User Registration...")
    user_data = {
        "username": f"vercel_user_{int(__import__('time').time())}",
        "email": f"vercel_{int(__import__('time').time())}@example.com",
        "password": "password123"
    }
    try:
        response = requests.post(f"{BASE_URL}/api/register", json=user_data, timeout=30)
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    except Exception as e:
        print(f"Error: {e}")
    
    # Test 4: Login User
    print("\n4. Testing User Login...")
    login_data = {
        "username": user_data["username"],
        "password": user_data["password"]
    }
    try:
        session = requests.Session()
        response = session.post(f"{BASE_URL}/api/login", json=login_data, timeout=30)
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        
        if response.status_code == 200:
            # Test 5: Get Profile (Protected Route)
            print("\n5. Testing User Profile...")
            response = session.get(f"{BASE_URL}/api/profile", timeout=30)
            print(f"Status: {response.status_code}")
            print(f"Response: {json.dumps(response.json(), indent=2)}")
            
            # Test 6: Create Post (Protected Route)
            print("\n6. Testing Create Post...")
            post_data = {
                "title": "Posted from Vercel!",
                "content": "This post was created on a Flask app running on Vercel serverless platform!"
            }
            response = session.post(f"{BASE_URL}/api/posts", json=post_data, timeout=30)
            print(f"Status: {response.status_code}")
            print(f"Response: {json.dumps(response.json(), indent=2)}")
        
    except Exception as e:
        print(f"Error: {e}")
    
    # Test 7: Get All Users
    print("\n7. Testing Get All Users...")
    try:
        response = requests.get(f"{BASE_URL}/api/users?page=1&per_page=5", timeout=30)
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    except Exception as e:
        print(f"Error: {e}")
    
    # Test 8: Get All Posts
    print("\n8. Testing Get All Posts...")
    try:
        response = requests.get(f"{BASE_URL}/api/posts?page=1&per_page=5", timeout=30)
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    except Exception as e:
        print(f"Error: {e}")
    
    print("\n" + "=" * 60)
    print("✅ Vercel API Testing Complete!")
    print(f"🌐 Your API is running at: {BASE_URL}")

if __name__ == "__main__":
    test_vercel_api()
