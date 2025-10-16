# test_complete_workflow.py
import requests
import json
import random

BASE_URL = "http://127.0.0.1:8000"

class StoryGenieTester:
    def __init__(self):
        self.token = None
        self.user_data = None
    
    def register_new_user(self):
        """Register a new test user"""
        random_id = random.randint(10000, 99999)
        user_data = {
            "username": f"testuser{random_id}",
            "email": f"test{random_id}@example.com",
            "password": "test123",
            "preferred_language": "en"
        }
        
        print(f"👤 Registering new user: {user_data['email']}")
        response = requests.post(f"{BASE_URL}/api/v1/auth/register", json=user_data)
        
        if response.status_code == 200:
            self.user_data = user_data
            self.token = response.json()["access_token"]
            print("✅ Registration successful!")
            return True
        else:
            print(f"❌ Registration failed: {response.json()}")
            return False
    
    def login(self, email, password):
        """Login with existing user"""
        login_data = {"email": email, "password": password}
        
        print(f"🔐 Logging in: {email}")
        response = requests.post(f"{BASE_URL}/api/v1/auth/login", json=login_data)
        
        if response.status_code == 200:
            self.token = response.json()["access_token"]
            print("✅ Login successful!")
            return True
        else:
            print(f"❌ Login failed: {response.json()}")
            return False
    
    def get_headers(self):
        """Get headers with authorization token"""
        return {"Authorization": f"Bearer {self.token}"}
    
    def generate_story(self, story_data):
        """Generate a new story"""
        print(f"📖 Generating {story_data['language']} {story_data['genre']} story...")
        
        response = requests.post(
            f"{BASE_URL}/api/v1/stories/generate",
            json=story_data,
            headers=self.get_headers()
        )
        
        if response.status_code == 200:
            story = response.json()["story"]
            print(f"✅ Story generated! Title: {story['title']}")
            print(f"   Words: {story['word_count']}, Language: {story['language']}")
            return story
        else:
            print(f"❌ Story generation failed: {response.json()}")
            return None
    
    def get_all_stories(self):
        """Get all user stories"""
        print("📚 Retrieving user stories...")
        response = requests.get(f"{BASE_URL}/api/v1/stories/", headers=self.get_headers())
        
        if response.status_code == 200:
            result = response.json()
            stories = result["stories"]
            print(f"✅ Found {len(stories)} stories")
            
            # Display stories in a nice format
            for i, story in enumerate(stories, 1):
                print(f"   {i}. '{story['title']}' - {story['genre']} ({story['language']}) - {story['word_count']} words")
            
            return stories
        else:
            print(f"❌ Failed to get stories: {response.json()}")
            return []
    
    def get_story_by_id(self, story_id):
        """Get a specific story by ID"""
        print(f"🔍 Getting story: {story_id}")
        response = requests.get(f"{BASE_URL}/api/v1/stories/{story_id}", headers=self.get_headers())
        
        if response.status_code == 200:
            story = response.json()["story"]
            print(f"✅ Story retrieved: {story['title']}")
            print(f"📝 Content preview: {story['content'][:100]}...")
            return story
        else:
            print(f"❌ Failed to get story: {response.json()}")
            return None
    
    def test_complete_workflow(self):
        """Test the complete user workflow"""
        print("🚀 Testing Complete StoryGenie Workflow")
        print("=" * 60)
        
        # Test 1: Register and login
        if not self.register_new_user():
            return
        
        print("\n" + "=" * 60)
        print("🌍 Testing Multi-Language Story Generation")
        print("=" * 60)
        
        # Test 2: Generate stories in different languages
        test_stories = [
            {
                "name": "English Fantasy",
                "data": {
                    "prompt": "A young mage discovers they can talk to animals",
                    "genre": "fantasy",
                    "language": "en",
                    "length": "medium",
                    "tone": "light_hearted",
                    "characters": ["young mage", "wise owl", "mischievous fox"],
                    "setting": "enchanted forest during autumn"
                }
            },
            {
                "name": "Hindi Sci-Fi", 
                "data": {
                    "prompt": "एक युवा वैज्ञानिक समय यात्रा की मशीन बनाता है",
                    "genre": "sci-fi",
                    "language": "hi",
                    "length": "short",
                    "tone": "serious",
                    "characters": ["युवा वैज्ञानिक", "भविष्य का यात्री"],
                    "setting": "वैज्ञानिक प्रयोगशाला"
                }
            },
            {
                "name": "Telugu Romance",
                "data": {
                    "prompt": "ఇద్దరు యువకులు ప్రాచీన దేవాలయంలో కలుసుకుంటారు",
                    "genre": "romance", 
                    "language": "te",
                    "length": "short",
                    "tone": "dramatic",
                    "characters": ["యువకుడు", "యువతి"],
                    "setting": "ప్రాచీన దేవాలయం"
                }
            }
        ]
        
        generated_stories = []
        for test in test_stories:
            print(f"\n🧪 {test['name']}")
            story = self.generate_story(test["data"])
            if story:
                generated_stories.append(story)
        
        print("\n" + "=" * 60)
        print("📊 Testing Story Retrieval")
        print("=" * 60)
        
        # Test 3: Get all stories
        all_stories = self.get_all_stories()
        
        # Test 4: Get a specific story
        if generated_stories:
            print(f"\n🔍 Testing specific story retrieval...")
            first_story = generated_stories[0]
            retrieved_story = self.get_story_by_id(first_story["id"])
        
        print("\n" + "=" * 60)
        print("🎉 WORKFLOW TEST COMPLETE!")
        print("=" * 60)
        
        # Summary
        total_words = sum(story.get('word_count', 0) for story in all_stories)
        languages = set(story['language'] for story in all_stories)
        genres = set(story['genre'] for story in all_stories)
        
        print(f"📈 Summary:")
        print(f"   • Total stories: {len(all_stories)}")
        print(f"   • Total words: {total_words}")
        print(f"   • Languages used: {', '.join(languages)}")
        print(f"   • Genres explored: {', '.join(genres)}")

def main():
    tester = StoryGenieTester()
    tester.test_complete_workflow()

if __name__ == "__main__":
    main()