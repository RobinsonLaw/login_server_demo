import requests
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Base URL for the Flask server
BASE_URL = "http://localhost:5000"

def test_api():
    print("🧪 Testing Flask API Server with SQLAlchemy")
    print("=" * 60)
    
    # Test 1: Health Check
    print("\n1. Testing Health Check...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    except Exception as e:
        print(f"Error: {e}")
    
    # Test 2: Register User
    print("\n2. Testing User Registration...")
    user_data = {
        "username": "sqlalchemy_user",
        "email": "sqlalchemy@example.com",
        "password": "password123"
    }
    try:
        response = requests.post(f"{BASE_URL}/register", json=user_data)
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    except Exception as e:
        print(f"Error: {e}")
    
    # Test 3: Login User
    print("\n3. Testing User Login...")
    login_data = {
        "username": "sqlalchemy_user",
        "password": "password123"
    }
    try:
        session = requests.Session()
        response = session.post(f"{BASE_URL}/login", json=login_data)
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        
        if response.status_code == 200:
            user_id = response.json()['user']['id']
            
            # Test 4: Get Profile (Protected Route)
            print("\n4. Testing User Profile...")
            response = session.get(f"{BASE_URL}/profile")
            print(f"Status: {response.status_code}")
            print(f"Response: {json.dumps(response.json(), indent=2)}")
            
            # Test 5: Update Profile (Protected Route)
            print("\n5. Testing Update Profile...")
            update_data = {"email": "updated_sqlalchemy@example.com"}
            response = session.put(f"{BASE_URL}/profile", json=update_data)
            print(f"Status: {response.status_code}")
            print(f"Response: {json.dumps(response.json(), indent=2)}")
            
            # Test 6: Create Post (Protected Route)
            print("\n6. Testing Create Post...")
            post_data = {
                "title": "SQLAlchemy is Awesome!",
                "content": "This post was created using Flask-SQLAlchemy ORM. It's much cleaner than raw SQL!"
            }
            response = session.post(f"{BASE_URL}/posts", json=post_data)
            print(f"Status: {response.status_code}")
            print(f"Response: {json.dumps(response.json(), indent=2)}")
            
            post_id = None
            if response.status_code == 201:
                post_id = response.json().get('post', {}).get('id')
            
            # Test 7: Update Post (Protected Route)
            if post_id:
                print(f"\n7. Testing Update Post (ID: {post_id})...")
                update_data = {
                    "title": "Updated: SQLAlchemy is Amazing!",
                    "content": "This post has been updated using SQLAlchemy ORM!"
                }
                response = session.put(f"{BASE_URL}/posts/{post_id}", json=update_data)
                print(f"Status: {response.status_code}")
                print(f"Response: {json.dumps(response.json(), indent=2)}")
            
            # Test 8: Get User's Posts
            print(f"\n8. Testing Get User's Posts (User ID: {user_id})...")
            response = requests.get(f"{BASE_URL}/users/{user_id}/posts")
            print(f"Status: {response.status_code}")
            print(f"Response: {json.dumps(response.json(), indent=2)}")
        
    except Exception as e:
        print(f"Error: {e}")
    
    # Test 9: Search Posts
    print("\n9. Testing Search Posts...")
    try:
        response = requests.get(f"{BASE_URL}/posts/search?q=SQLAlchemy")
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    except Exception as e:
        print(f"Error: {e}")
    
    # Test 10: Get All Users (with pagination)
    print("\n10. Testing Get All Users...")
    try:
        response = requests.get(f"{BASE_URL}/users?page=1&per_page=5")
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    except Exception as e:
        print(f"Error: {e}")
    
    # Test 11: Get All Posts (with pagination)
    print("\n11. Testing Get All Posts...")
    try:
        response = requests.get(f"{BASE_URL}/posts?page=1&per_page=5")
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    except Exception as e:
        print(f"Error: {e}")
    
    print("\n" + "=" * 60)
    print("✅ SQLAlchemy API Testing Complete!")

if __name__ == "__main__":
    test_api()
