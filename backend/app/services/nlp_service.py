# D:\Research Teaser Intenship\Project\Story\backend\app\services\nlp_service.py
import logging
import asyncio
import torch
from transformers import (
    AutoModelForCausalLM, AutoTokenizer,
    AutoConfig,
)
from transformers.pipelines import Pipeline as PipelineClass
from peft import PeftModel
from typing import Dict, Any, Optional, List
from concurrent.futures import ThreadPoolExecutor
import os
import traceback

from app.core.config import settings

logger = logging.getLogger(__name__)

# --- Configuration for LoRA Weights ---
LORA_WEIGHTS_PATH = os.environ.get("LORA_WEIGHTS_PATH", "./lora_storygenie_weights")


# --- Helper function for synchronous (blocking) model loading ---
def _load_model_sync(config: Dict[str, Any], cache_dir: str):
    """
    Synchronous function to load tokenizer, base model (Gemma 2B), 
    and conditionally apply LoRA weights for inference.
    """
    model_name = config['model_name']
    
    device = "cuda" if torch.cuda.is_available() else "cpu"
    dtype = torch.float16
        
    logging.info(f"Loading model on {device} with dtype={dtype}")

    # 1. Load Tokenizer
    tokenizer = AutoTokenizer.from_pretrained(
        model_name,
        cache_dir=cache_dir,
        token=settings.HUGGINGFACE_API_KEY
    )

    if not tokenizer.pad_token:
        tokenizer.pad_token = tokenizer.eos_token
        
    tokenizer.padding_side = "left"

    # 2. Load Base Model (Gemma 2B)
    model_config = AutoConfig.from_pretrained(model_name)
    
    base_model = AutoModelForCausalLM.from_pretrained(
        model_name,
        config=model_config,
        cache_dir=cache_dir,
        torch_dtype=dtype, 
        token=settings.HUGGINGFACE_API_KEY, 
        trust_remote_code=True,
        low_cpu_mem_usage=True if device == "cpu" else False 
    )
    
    # 3. LoRA Fine-Tuning Integration
    model = base_model
    if os.path.exists(LORA_WEIGHTS_PATH) and os.path.isdir(LORA_WEIGHTS_PATH):
        logger.info(f"💾 Found LoRA weights at {LORA_WEIGHTS_PATH}. Applying fine-tuning...")
        try:
            model = PeftModel.from_pretrained(base_model, LORA_WEIGHTS_PATH, is_trainable=False)
            model = model.merge_and_unload()
            logger.info("✅ LoRA weights merged into model successfully.")
        except Exception as e:
            logger.error(f"❌ Failed to load and merge LoRA weights: {e}. Falling back to base model.")
    else:
        logger.warning(f"⚠️ LoRA weights not found at {LORA_WEIGHTS_PATH}. Using base model.")

    if device == "cuda":
        model.to(device)

    model.config.pad_token_id = tokenizer.pad_token_id
    model.eval()
    return model, tokenizer

class NLPService:
    def __init__(self):
        self.is_initialized = False
        self.executor = ThreadPoolExecutor(max_workers=8) 
        self.models = {}
        self.tokenizers = {}
        
        self.model_configs = {
            "main": {
                "model_name": "google/gemma-2-2b-it", 
                "description": "Gemma 2 2B for multilingual stories"
            }
        }
        # Load high-quality examples with clear template markers
        self.few_shot_examples = self._load_few_shot_examples()


    def _load_few_shot_examples(self) -> Dict[str, str]:
        """Defines and loads few-shot examples structured using the full Gemma template."""
        # The content of the example is the full input/output turn
        return {
            "hi_mystery": 
                "<start_of_turn>user\n"
                "**INSTRUCTIONS:** You are a professional author. Your task is to write a medium-length story (around 400 words) in the **MYSTERY** genre, strictly maintaining a **Serious** tone. The final story must be entirely in **Hindi**. Do not include any titles, introductory phrases, or concluding remarks like 'The End'. Begin immediately with the story's first sentence.\n"
                "**STORY IDEA:** एक पत्रकार को एक गायब हो चुके लेखक की अंतिम पांडुलिपि मिलती है, जिसमें उसकी खुद की गायब होने की योजना विस्तार से लिखी है.\n"
                "<end_of_turn>\n<start_of_turn>model\n"
                "पुराने टाइपराइटर की दराज से धूल साफ करते हुए, पत्रकार आकाश ने वह पांडुलिपि पाई जिसकी तलाश पूरी पुलिस और मीडिया को थी—गायब हो चुके लेखक विक्रम वर्मा का अंतिम काम। यह पांडुलिपि विक्रम के अगले उपन्यास का पहला अध्याय होना चाहिए था, लेकिन जैसे ही आकाश ने पढ़ना शुरू किया, उसके हाथ ठंडे पड़ गए। ... एक कहानीकार के अंतिम नाटक को क्यों खराब करना? शायद उसे बस इसे दुनिया के लिए एक रहस्य बने रहने देना चाहिए।\n",
            
            "te_comedy":
                "<start_of_turn>user\n"
                "**INSTRUCTIONS:** You are a professional author. Your task is to write a short story (around 200 words) in the **COMEDY** genre, strictly maintaining a **Humorous** tone. The final story must be entirely in **Telugu**. Do not include any titles, introductory phrases, or concluding remarks like 'The End'. Begin immediately with the story's first sentence.\n"
                "**STORY IDEA:** ఒక పిల్లి తన యజమాని యొక్క అన్ని రహస్యాలను బహిరంగంగా చెబుతుంది, కానీ ఎవరూ నమ్మరు.\n"
                "<end_of_turn>\n<start_of_turn>model\n"
                "బంగారం అనే పిల్లికి ఒక అలవాటు ఉంది: అది మనుషుల్లా మాట్లాడగలదు, కానీ దాని యజమాని నరసింహరావు దాన్ని ఎప్పుడూ మూతి ముడుచుకునే చూసేవాడు. నరసింహరావు గొప్ప రహస్యాలు ఉన్న మనిషి, ముఖ్యంగా పక్కింటి వెంకటేశ్వర రావు నుండి అతను అప్పు తీసుకున్న విషయం. ... నరసింహరావు అప్పు రహస్యం చివరకు ఎవరికీ అర్థం కాలేదు, ఎందుకంటే, ఎవరో చెప్పారంటే ఎవరు నమ్ముతారు?\n",
            
            "en_fantasy":
                "<start_of_turn>user\n"
                "**INSTRUCTIONS:** You are a professional author. Your task is to write a medium-length story (around 400 words) in the **FANTASY** genre, strictly maintaining a **Light Hearted** tone. The final story must be entirely in **English**. Do not include any titles, introductory phrases, or concluding remarks like 'The End'. Begin immediately with the story's first sentence.\n"
                "**STORY IDEA:** You discover a door in your house that wasn't there yesterday.\n"
                "<end_of_turn>\n<start_of_turn>model\n"
                "Dust motes danced in the afternoon sunbeams, illuminating the worn rug beneath my feet. My eyes drifted from the antique gramophone perched precariously on the shelf to the chipped floral wallpaper peeling at the edges of the dining room. ... I stood at the edge of a vibrant meadow, bathed in the golden glow of a double rainbow. The scent of honey and cinnamon hung thick in the air, and a chorus of birdsong filled the symphony of nature.\n"
        }
    
    async def _load_main_model(self):
        key = "main"
        try:
            config = self.model_configs[key]
            logger.info(f"📥 Loading main model: {config['model_name']}")
            
            loop = asyncio.get_event_loop()
            model, tokenizer = await loop.run_in_executor(
                self.executor,
                lambda: _load_model_sync(config, settings.MODEL_CACHE_DIR)
            )
            
            for lang in ["en", "hi", "te"]:
                 self.tokenizers[lang] = tokenizer
                 self.models[lang] = model
                 
            logger.info(f"✅ Main model loaded and successfully assigned to en, hi, te.")
            
        except Exception as e:
            logger.error(f"❌ Failed to load main model: {e}")
            raise 

    async def initialize(self):
        try:
            logger.info("🚀 Initializing NLP Service with Local Models...")
            await self._load_main_model() 
            
            self.is_initialized = True
            logger.info("✅ NLP Service initialized successfully")
            
        except Exception as e:
            logger.error(f"❌ NLP Service initialization failed: {e}")
            self.is_initialized = False 
            raise 

    async def generate_story(self, story_data: Dict[str, Any]) -> str:
        
        if not self.is_initialized or "en" not in self.models:
            return "❌ AI service is not ready. Please check backend logs for model loading status."
            
        try:
            prompt = story_data['prompt']
            language = story_data['language']
            genre = story_data['genre']
            length = story_data['length']
            tone = story_data.get('tone', 'light_hearted')
            
            logger.info(f"🔄 Generating {language} story using local AI model...")
            
            enhanced_prompt = self._build_gemma_prompt(
                prompt, language, genre, 
                tone, length, 
                story_data.get('characters'), 
                story_data.get('setting')
            )
            
            generated_text = await self._generate_with_direct_model(language, enhanced_prompt, length)
            
            if generated_text:
                # Use Few-Shot and Gemma-specific cleaning logic
                cleaned_text = self._clean_gemma_generated_text(generated_text)
                
                if len(cleaned_text.strip()) > 50:
                    logger.info(f"✅ AI-generated {language} story: {len(cleaned_text)} chars")
                    return cleaned_text
                
            error_msg = "❌ AI story generation failed. Final text too short or empty. Try a different prompt."
            logger.error(f"❌ AI story generation failed for language={language}. Final text too short or empty.") 
            return error_msg
            
        except Exception as e:
            logger.error(f"❌ Story generation CRITICAL ERROR: {str(e)}", exc_info=True) 
            return "❌ AI story generation failed due to an internal error. Please check logs."
    
    def _build_gemma_prompt(self, prompt: str, language: str, genre: str, tone: str, length: str, characters: Optional[List[str]], setting: Optional[str]) -> str:
        """
        Builds a structured prompt using the Google Gemma Instruct format,
        implementing Few-Shot demonstration with clear structural markers.
        """
        
        # 1. Select the relevant example
        example_key = f"{language}_{genre.lower()}"
        few_shot_demo = self.few_shot_examples.get(example_key, None)
        
        # Fallback logic: Use English Fantasy as a structural guide if the specific language/genre is missing
        if few_shot_demo is None:
             few_shot_demo = self.few_shot_examples.get("en_fantasy", None)

        # --- Setup the NEW Task Instructions ---
        language_names = { "en": "English", "hi": "Hindi", "te": "Telugu" }
        word_count_map = {
            "short": "a short story (around 200 words)",
            "medium": "a medium-length story (around 400 words)",
            "long": "a long and detailed story (around 600 words)"
        }
        
        system_instruction_new = (
            f"You are a professional author and master storyteller. Your task is to write {word_count_map.get(length, 'a medium-length story')} "
            f"in the **{genre.upper()}** genre, strictly maintaining a **{tone.replace('_', ' ').title()}** tone. "
            f"The final story must be entirely in **{language_names.get(language, 'language')}**. "
            f"Do not include any titles, introductory phrases, or concluding remarks like 'The End'. "
            f"Begin immediately with the story's first sentence."
        )
        
        user_message_new = f"Write the story based on this central plot idea: '{prompt}'"
        
        if characters:
            user_message_new += f"\n- Main Characters: {', '.join(characters)}"
        if setting:
            user_message_new += f"\n- Setting: {setting}"

        # 2. Construct the Final Prompt with XML-like Delineation
        final_prompt = "<bos>"
        
        if few_shot_demo:
             # Structure: Use tags to clearly separate the demonstration from the current task
             final_prompt += (
                 "\n<EXAMPLE_START>\n"
                 f"{few_shot_demo}"
                 "\n<EXAMPLE_END>\n\n"
             )
        
        # Add the actual NEW task
        final_prompt += (
            "<start_of_turn>user\n"
            f"**INSTRUCTIONS:** {system_instruction_new}\n"
            f"**STORY IDEA:** {user_message_new}"
            "<end_of_turn>\n<start_of_turn>model\n"
        )
        
        return final_prompt
    
    async def _generate_with_direct_model(self, language: str, prompt: str, length: str) -> str:
        """Generate using direct model access (runs synchronously in thread)."""
        try:
            model = self.models[language]
            tokenizer = self.tokenizers[language]
            
            max_input_length = 1024 
            inputs = tokenizer.encode(prompt, return_tensors="pt", truncation=True, max_length=max_input_length)
            
            if torch.cuda.is_available():
                inputs = inputs.to(model.device)
            
            # Generation configuration is optimized for creative, controlled output
            generation_config = {
                "max_new_tokens": self._get_token_length(length),
                "temperature": 0.9, 
                "do_sample": True, 
                "top_p": 0.9, 
                "top_k": 40, 
                "repetition_penalty": 1.1, 
                "pad_token_id": tokenizer.pad_token_id,
                "eos_token_id": tokenizer.eos_token_id, 
                "num_return_sequences": 1,
            }
            
            loop = asyncio.get_event_loop()
            
            def generate_direct_sync():
                with torch.no_grad():
                    return model.generate(
                        inputs, 
                        **generation_config,
                        attention_mask=(inputs != tokenizer.pad_token_id)
                    )

            outputs = await loop.run_in_executor(self.executor, generate_direct_sync)
            
            return tokenizer.decode(outputs[0], skip_special_tokens=False) 
            
        except Exception as e:
            logger.error(f"❌ Direct model generation failed for {language}: {e}", exc_info=True)
            return None
    
    def _get_token_length(self, length: str) -> int:
        """Translates abstract length to maximum new tokens."""
        return {
            "short": 300,
            "medium": 500,
            "long": 700
        }.get(length, 400)
    
    def _clean_gemma_generated_text(self, generated_text: str) -> str:
        """
        Aggressively removes all input artifacts (Few-Shot examples, current prompt, 
        and special tokens) from the generated text, ensuring only the new story remains.
        """
        story_text = generated_text.strip()
    
    # 1. Strip everything *before* the start of the final model generation turn.
    # The actual new story content starts immediately after the final "<start_of_turn>model\n" tag.
        final_model_marker = "<start_of_turn>model\n"
        if final_model_marker in story_text:
        # Find the last occurrence, which marks the start of the new response.
            start_index = story_text.rfind(final_model_marker) + len(final_model_marker)
            story_text = story_text[start_index:].strip()
    
    # 2. Remove all Few-Shot Delineation Tags (Just in case they remain)
    # This specifically targets the EXAMPLE_START marker and anything before it.
        story_text = story_text.split("<EXAMPLE_START>")[0].strip()
        story_text = story_text.split("<EXAMPLE_END>")[0].strip()
    
    # 3. Remove all Gemma special tokens and instruction markers (Final scrubbing)
        special_tokens_to_remove = ["<bos>", "<eos>", "<start_of_turn>", "<end_of_turn>", "user", "model", "**INSTRUCTIONS:**", "**STORY IDEA:**", "<EXAMPLE_START>", "<EXAMPLE_END>"]
    
        for token in special_tokens_to_remove:
        # Use str.replace aggressively
            story_text = story_text.replace(token, "").strip()

    # 4. Final cleanup for formatting
        lines = []
        for line in story_text.split('\n'):
            clean_line = line.strip()
        # Filter noise lines and empty lines
            if clean_line and len(clean_line.split()) > 4: 
                lines.append(clean_line)
    
        cleaned_text = '\n\n'.join(lines)

    # Ensure the story ends with punctuation
        if cleaned_text and cleaned_text.strip() and not cleaned_text.strip()[-1] in '.!?"\'।':
            cleaned_text += '.'
        
        return cleaned_text.strip()


    async def close(self):
        """Shuts down the executor and clears resources."""
        try:
            if hasattr(self, 'executor'):
                self.executor.shutdown(wait=True)
            
            for model in self.models.values():
                del model
            
            self.models.clear()
            self.tokenizers.clear()
            
            if torch.cuda.is_available():
                torch.cuda.empty_cache()
            
            logger.info("✅ NLP Service closed successfully")
        except Exception as e:
            logger.error(f"❌ Error closing NLP service: {e}")

# Global instance
nlp_service = NLPService()