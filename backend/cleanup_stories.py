# cleanup_stories.py
import requests
import json

BASE_URL = "http://127.0.0.1:8000"

def cleanup_zero_word_stories():
    """Clean up stories with 0 word count"""
    
    # Login
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
    
    # Get all stories
    response = requests.get(f"{BASE_URL}/api/v1/stories/", headers=headers)
    if response.status_code != 200:
        print("❌ Failed to get stories")
        return
    
    stories = response.json()["stories"]
    zero_word_stories = [s for s in stories if s.get('word_count', 0) == 0]
    
    print(f"Found {len(zero_word_stories)} stories with 0 word count")
    
    # Note: In a real application, you'd have a DELETE endpoint
    # For now, we'll just list them
    for story in zero_word_stories:
        print(f"⚠️  Zero-word story: {story['title']} (ID: {story['id']})")

if __name__ == "__main__":
    cleanup_zero_word_stories()