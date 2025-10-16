# test_story_generation.py
import requests
import json

BASE_URL = "http://127.0.0.1:8000"

def test_story_generation():
    """Test story generation with authentication"""
    
    # Login credentials
    login_data = {
        "email": "test4241@example.com",
        "password": "test123"
    }
    
    try:
        print("🔐 Logging in...")
        # Login to get token
        response = requests.post(f"{BASE_URL}/api/v1/auth/login", json=login_data)
        
        if response.status_code != 200:
            print(f"❌ Login failed: {response.json()}")
            return
        
        login_response = response.json()
        token = login_response["access_token"]
        user = login_response["user"]
        
        print(f"✅ Logged in as: {user['username']}")
        print(f"🔑 Token: {token[:50]}...")
        
        # Set up headers with authorization
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        
        # Story data
        story_data = {
            "prompt": "A young wizard discovers a magical book in an ancient library that can predict the future",
            "genre": "fantasy",
            "language": "en",
            "length": "short",
            "tone": "dramatic",
            "characters": ["young wizard", "wise old librarian", "mysterious stranger"],
            "setting": "ancient magical library with floating books"
        }
        
        print("\n📖 Generating story...")
        print(f"Prompt: {story_data['prompt']}")
        print(f"Genre: {story_data['genre']}")
        print(f"Language: {story_data['language']}")
        
        # Generate story
        response = requests.post(
            f"{BASE_URL}/api/v1/stories/generate", 
            json=story_data,
            headers=headers
        )
        
        print(f"\n📊 Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            story = result["story"]
            
            print("✅ Story generation successful!")
            print(f"📚 Title: {story['title']}")
            print(f"🔤 Word Count: {story['word_count']}")
            print(f"🎭 Genre: {story['genre']}")
            print(f"🌍 Language: {story['language']}")
            print(f"📝 Content Preview:")
            print("-" * 50)
            print(story['content'])
            print("-" * 50)
            
        else:
            print(f"❌ Story generation failed: {response.json()}")
            
    except Exception as e:
        print(f"💥 Error: {e}")

def test_multi_language_stories():
    """Test story generation in different languages"""
    
    # Login first
    login_data = {
        "email": "test4241@example.com",
        "password": "test123"
    }
    
    response = requests.post(f"{BASE_URL}/api/v1/auth/login", json=login_data)
    if response.status_code != 200:
        return
    
    token = response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    # Test different languages
    test_cases = [
        {
            "name": "English Fantasy",
            "data": {
                "prompt": "A dragon and a knight become unlikely friends",
                "genre": "fantasy", 
                "language": "en",
                "length": "short",
                "tone": "light_hearted",
                "characters": ["brave knight", "friendly dragon"],
                "setting": "enchanted forest"
            }
        },
        {
            "name": "Hindi Mystery", 
            "data": {
                "prompt": "एक रहस्यमय घर जहां रोज नई घटनाएं होती हैं",
                "genre": "mystery",
                "language": "hi",
                "length": "medium", 
                "tone": "dramatic",
                "characters": ["जासूस", "रहस्यमय व्यक्ति"],
                "setting": "पुराना हवेली"
            }
        },
        {
            "name": "Telugu Adventure",
            "data": {
                "prompt": "ఒక యువకుడు ప్రాచీన నగరంలో గుప్త నిధిని కనుగొంటాడు",
                "genre": "adventure",
                "language": "te", 
                "length": "short",
                "tone": "serious",
                "characters": ["యువకుడు", "మార్గదర్శి"],
                "setting": "ప్రాచీన నగరం"
            }
        }
    ]
    
    for test_case in test_cases:
        print(f"\n🧪 Testing: {test_case['name']}")
        response = requests.post(
            f"{BASE_URL}/api/v1/stories/generate",
            json=test_case["data"],
            headers=headers
        )
        
        if response.status_code == 200:
            story = response.json()["story"]
            print(f"✅ Success! Words: {story['word_count']}")
            print(f"📖 Preview: {story['content'][:100]}...")
        else:
            print(f"❌ Failed: {response.json()}")

if __name__ == "__main__":
    print("🚀 Testing Story Generation API")
    print("=" * 60)
    
    # Test basic story generation
    test_story_generation()
    
    print("\n" + "=" * 60)
    print("🌍 Testing Multi-Language Support")
    print("=" * 60)
    
    # Test multiple languages
    test_multi_language_stories()