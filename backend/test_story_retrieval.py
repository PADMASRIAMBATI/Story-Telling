# test_story_retrieval.py
import requests
import json

BASE_URL = "http://127.0.0.1:8000"

def test_get_stories():
    """Test retrieving user stories"""
    
    # Login first
    login_data = {
        "email": "test4241@example.com",
        "password": "test123"
    }
    
    response = requests.post(f"{BASE_URL}/api/v1/auth/login", json=login_data)
    if response.status_code != 200:
        print("❌ Login failed")
        return
    
    token = response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    # Get user stories
    response = requests.get(f"{BASE_URL}/api/v1/stories/", headers=headers)
    
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print(f"✅ Retrieved {result['total_count']} stories")
        for story in result["stories"]:
            print(f"📖 {story['title']} - {story['genre']} - {story['word_count']} words")
    else:
        print(f"❌ Failed: {response.json()}")

if __name__ == "__main__":
    test_get_stories()