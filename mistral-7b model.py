from transformers import pipeline, set_seed
import torch
import re

def create_story_generator():
    """Initialize the text generation pipeline with optimized settings."""
    try:
        device = 0 if torch.cuda.is_available() else -1
        print(f"Device set to use {'gpu' if device == 0 else 'cpu'}")
        
        
        generator = pipeline(
            'text-generation', 
            model='mistral-7b', 
            device=device,
            return_full_text=False  
        )
        return generator
    except Exception as e:
        print(f"Error loading model: {e}")
       
        try:
            generator = pipeline('text-generation', model='gpt2', device=device, return_full_text=False)
            return generator
        except:
            return None

def clean_and_structure_text(text, prompt):
    """Clean and structure the generated text."""
   
    text = text.replace(prompt, "").strip()
    
    
    sentences = re.split(r'[.!?]+', text)
    cleaned_sentences = []
    
    for sentence in sentences:
        sentence = sentence.strip()
        if sentence and len(sentence) > 10:  
            
            sentence = sentence[0].upper() + sentence[1:] if len(sentence) > 1 else sentence.upper()
            cleaned_sentences.append(sentence)
    
    
    result = '. '.join(cleaned_sentences[:5])  
    if result and not result.endswith(('.', '!', '?')):
        result += '.'
    
    return result

def generate_structured_story(generator, prompt, length_category="medium"):
    """Generate a well-structured story."""
    
    
    length_configs = {
        "short": {"max_new_tokens": 180, "num_sentences": 3},
        "medium": {"max_new_tokens": 320, "num_sentences": 5},
        "long": {"max_new_tokens": 580, "num_sentences": 7}
    }
    
    config = length_configs.get(length_category, length_configs["medium"])
    
    
    story_prompt = f"Here is a story: {prompt.strip()}"
    if not story_prompt.endswith(('.', '!', '?')):
        story_prompt += "."
    
    try:
        
        result = generator(
            story_prompt,
            max_new_tokens=config["max_new_tokens"],
            do_sample=True,
            temperature=0.7,  
            top_p=0.9,        
            top_k=50,        
            repetition_penalty=1.2,  
            pad_token_id=generator.tokenizer.eos_token_id,
            truncation=True,
            no_repeat_ngram_size=3  
        )
        
        generated_text = result[0]['generated_text']
        
        
        cleaned_story = clean_and_structure_text(generated_text, prompt)
        
        return cleaned_story
        
    except Exception as e:
        print(f"Error generating story: {e}")
        return None

def main():
    print("📚 Enhanced AI Story Generator")
    print("=" * 40)
    
    
    set_seed(42)
    
    
    print("Loading model...")
    generator = create_story_generator()
    
    if not generator:
        print("❌ Failed to load the model. Please check your installation.")
        return
    
    print("✅ Model loaded successfully!\n")
    
    while True:
        print("-" * 40)
        prompt = input("📝 Enter your story prompt (or 'quit' to exit): ").strip()
        
        if prompt.lower() in ['quit', 'exit', 'q']:
            print("👋 Thanks for using the story generator!")
            break
            
        if not prompt:
            print("⚠️  Please enter a valid prompt.\n")
            continue
        
        
        print("\nChoose story length:")
        print("1️⃣  Short (3-4 sentences)")
        print("2️⃣  Medium (4-6 sentences)")  
        print("3️⃣  Long (6-8 sentences)")
        
        length_choice = input("Enter choice (1-3, default 2): ").strip()
        length_map = {"1": "short", "2": "medium", "3": "long"}
        length_category = length_map.get(length_choice, "medium")
        
        print(f"\n🤖 Generating {length_category} story...")
        
        
        story = generate_structured_story(generator, prompt, length_category)
        
        if story and story.strip():
            print("\n" + "="*60)
            print("📖 Generated Story:")
            print("="*60)
            print(f"\n{story}\n")
            print("="*60 + "\n")
        else:
            print("❌ Failed to generate a good story. Please try a different prompt.\n")

if __name__ == "__main__":
    main()