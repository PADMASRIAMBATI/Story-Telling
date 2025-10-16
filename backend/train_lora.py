import os
import torch
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    # BitsAndBytesConfig removed as it causes CPU deadlocks
    TrainingArguments
)
from peft import LoraConfig
from trl import SFTTrainer
from datasets import load_dataset
import logging

# --- Configuration Setup ---
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Constants (Must be small for CPU stability)
MODEL_ID = "google/gemma-2-2b-it"
DATASET_PATH = "story_training_data.json" 
OUTPUT_DIR = "./lora_storygenie_weights" 
LOGS_DIR = "./lora_storygenie_logs"
NUM_EPOCHS = 1             # Minimal epochs for fast testing (Can be increased to 3 later)
MAX_SEQ_LENGTH = 1024      # Max token length
PER_DEVICE_BATCH_SIZE = 1  # Absolute minimum batch size
GRADIENT_ACCUMULATION = 1  # Set to 1 to avoid high RAM use (was 4, caused stalls)


def train_lora_cpu_only():
    
    # 1. Load Dataset (Local JSON file)
    logger.info(f"Loading dataset from: {DATASET_PATH}")
    if not os.path.exists(DATASET_PATH):
        raise FileNotFoundError(f"Dataset not found at {DATASET_PATH}. Please create it.")
    
    # Dataset should contain a 'text' column formatted with the Gemma template
    dataset = load_dataset("json", data_files=DATASET_PATH, split="train")

    # 2. Load Model and Tokenizer (CPU Optimized)
    logger.info(f"Loading model: {MODEL_ID} in float16 for CPU stability...")
    
    # Explicitly map the model to CPU with half-precision (float16) to save RAM
    device_map = {"": "cpu"}

    model = AutoModelForCausalLM.from_pretrained(
        MODEL_ID,
        device_map=device_map,
        trust_remote_code=True,
        torch_dtype=torch.float16 # Half-precision to reduce memory footprint
    )
    
    tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)
    tokenizer.pad_token = tokenizer.eos_token
    tokenizer.padding_side = "right"

    # 3. Tokenize Dataset (Required preprocessing step)
    def tokenize_function(examples):
        return tokenizer(
            examples["text"],
            truncation=True,
            max_length=MAX_SEQ_LENGTH,
            padding="max_length"
        )
    
    logger.info(f"Tokenizing dataset and applying max length: {MAX_SEQ_LENGTH}...")
    tokenized_dataset = dataset.map(
        tokenize_function,
        batched=True,
        remove_columns=["text"],
    )

    # 4. Define LoRA Configuration
    logger.info("Defining LoRA configuration...")
    lora_config = LoraConfig(
        r=16, # Rank of the update matrices
        lora_alpha=32, 
        lora_dropout=0.05,
        target_modules=["q_proj", "o_proj", "v_proj", "k_proj", "down_proj", "up_proj"],
        bias="none",
        task_type="CAUSAL_LM", 
    )

    # 5. Define Training Arguments
    logger.info("Defining training arguments...")
    training_args = TrainingArguments(
        output_dir=LOGS_DIR,
        num_train_epochs=NUM_EPOCHS,
        per_device_train_batch_size=PER_DEVICE_BATCH_SIZE,  
        gradient_accumulation_steps=GRADIENT_ACCUMULATION, # Minimal accumulation for memory stability
        optim="adamw_torch", # Standard PyTorch optimizer (avoids bitsandbytes deadlock)
        learning_rate=2e-4,
        logging_steps=1, # Log every step, since there are so few
        save_strategy="epoch",
        fp16=True, # Use 16-bit math for speed and memory efficiency
        warmup_ratio=0.03,
        report_to="none",
    )

    # 6. Initialize and Start SFT Trainer
    logger.info("Initializing SFT Trainer...")
    trainer = SFTTrainer(
        model=model,
        args=training_args,
        train_dataset=tokenized_dataset,
        peft_config=lora_config, 
    )

    logger.info("Starting training...")
    trainer.train()

    # 7. Save LoRA Adapters
    logger.info(f"Training finished. Saving adapters to {OUTPUT_DIR}...")
    os.makedirs(OUTPUT_DIR, exist_ok=True) 
    trainer.model.save_pretrained(OUTPUT_DIR)
    tokenizer.save_pretrained(OUTPUT_DIR)
    logger.info("✅ LoRA fine-tuning complete and weights saved!")


if __name__ == "__main__":
    try:
        train_lora_cpu_only()
    except Exception as e:
        logger.error(f"❌ An error occurred during fine-tuning: {e}")