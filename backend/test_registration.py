import requests
import json

BASE_URL = "http://127.0.0.1:8000"

def test_registration():
    """Test user registration"""
    # Use a unique email each time to avoid duplicate errors
    import random
    random_id = random.randint(1000, 9999)
    
    user_data = {
        "username": f"testuser{random_id}",
        "email": f"test{random_id}@example.com",
        "password": "test123",  # Normal length password
        "preferred_language": "en"
    }
    
    try:
        print(f"Testing registration with email: {user_data['email']}")
        response = requests.post(f"{BASE_URL}/api/v1/auth/register", json=user_data)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ Registration successful!")
            print(f"Response: {json.dumps(response.json(), indent=2)}")
            return True, user_data
        else:
            print(f"❌ Registration failed: {response.json()}")
            return False, None
            
    except Exception as e:
        print(f"Error: {e}")
        return False, None

def test_login(user_data):
    """Test user login with the registered user"""
    if not user_data:
        print("❌ No user data for login test")
        return False
        
    login_data = {
        "email": user_data["email"],
        "password": user_data["password"]
    }
    
    try:
        print(f"Testing login with email: {login_data['email']}")
        response = requests.post(f"{BASE_URL}/api/v1/auth/login", json=login_data)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ Login successful!")
            print(f"Access Token: {response.json()['access_token'][:50]}...")
            return True
        else:
            print(f"❌ Login failed: {response.json()}")
            return False
            
    except Exception as e:
        print(f"Error: {e}")
        return False

if __name__ == "__main__":
    print("Testing StoryGenie Authentication...")
    print("=" * 50)
    
    # Test registration
    success, user_data = test_registration()
    
    if success:
        print("\n" + "=" * 50)
        # Test login with the same user
        test_login(user_data)