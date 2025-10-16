# download_models.py
import os
import sys
import requests
import torch 
from transformers import AutoModelForCausalLM, AutoTokenizer
# Assuming app.core.config is available to import settings and read the API key
from app.core.config import settings
import logging

# Set up basic logging for download status
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# --- Read Token for Authentication ---
AUTH_TOKEN = settings.HUGGINGFACE_API_KEY

if not AUTH_TOKEN:
    logging.error("HUGGINGFACE_API_KEY is missing from configuration. Cannot proceed.")
    sys.exit(1)

def download_model(model_name):
    """Verifies that the cached model files can be loaded without error."""
    logging.info(f"--- Starting verification of cached model: {model_name} ---")
        
    try:
        # 1. Verify Tokenizer
        tokenizer = AutoTokenizer.from_pretrained(
            model_name, 
            cache_dir=settings.MODEL_CACHE_DIR, 
            token=AUTH_TOKEN # Required for authenticated model verification
        )
        logging.info("✅ Tokenizer verified successfully.")
        
        # 2. Verify Model Weights
        # CRITICAL FIX: Removed the invalid 'request_timeout' argument here.
        # Use low precision (float16) to conserve memory during loading.
        model = AutoModelForCausalLM.from_pretrained(
            model_name, 
            cache_dir=settings.MODEL_CACHE_DIR,
            token=AUTH_TOKEN,
            torch_dtype=torch.float16 
        )
        logging.info(f"✅ Model weights for {model_name} verified successfully from cache.")
        
    except Exception as e:
        logging.error(f"❌ Verification failed for {model_name}.")
        logging.error(f"🚨 CRITICAL ERROR: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    # Rerunning the script to ensure the cache is fully verified without errors
    # Note: This will still take time as it loads 13GB into memory for verification.
    download_model("mistralai/Mistral-7B-Instruct-v0.2") 
    logging.info("--- Verification script finished running. ---")
