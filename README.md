
# 📖 StoryGenie: AI-Powered Multilingual Storytelling Platform

StoryGenie is a fully optimized **FastAPI backend** designed to generate high-quality, specialized creative fiction in **English, Hindi, and Telugu**. It utilizes a specialized, locally deployed Large Language Model (LLM) to ensure coherent and accurate narrative generation even on consumer hardware.

## 🚀 Key Features and Technology

| Component | Detail | Description |
| :--- | :--- | :--- |
| **Core Model** | **Gemma 2-2B Instruct** | The small, efficient open-source model optimized for laptop deployment. |
| **Specialization** | **QLoRA Fine-Tuning** | The model was trained on a custom multilingual dataset to **fix coherence and plot failures** in Hindi/Telugu. |
| **Deployment** | **LoRA Adapter Merging** | The specialized weights are merged into the base model during startup, activating custom capabilities. |
| **Quality Control** | **Few-Shot Prompting** | High-quality examples are used in the prompt to enforce strict adherence to genre and tone. |
| **Length Control** | **Aggressive Parameters** | Uses `repetition_penalty: 1.1` and `temperature: 0.9` to push stories toward the requested 400–600 word length. |
| **Backend / DB** | FastAPI (Python) / **MongoDB** | High-performance API layer with JWT authentication and history storage. |

-----

## 🛠️ Local Installation and Setup

### 1\. Prerequisites

Ensure you have Python 3.10+ and the following accounts set up:

  * **MongoDB** (Local or Cloud Atlas Cluster)
  * **Hugging Face Access Token** (Read permission required for model download)

### 2\. Clone and Initialize Project

```bash
# Clone your repository
git clone [YOUR_REPO_URL]
cd [YOUR_REPO_NAME]/backend

# Create and activate environment
python -m venv venv
source venv/bin/activate  # Use 'venv\Scripts\activate' on Windows
```

### 3\. Install Dependencies

Install all project requirements, including the necessary heavy AI and security libraries:

```bash
pip install -r requirements.txt
```

### 4\. Configuration (`.env` file)

Create a file named **`.env`** in the `backend` directory and fill in your keys:

```env
# .env file content
MONGODB_URI=your_mongodb_connection_string
DATABASE_NAME=storygenie
JWT_SECRET_KEY=your-super-secret-key-change-this
HUGGINGFACE_API_KEY=your_read_access_token 
```

### 5\. Deploy Fine-Tuned Weights (Crucial Step)

The specialized model weights **MUST** be placed in the root of the `backend` folder for the application to load them.

1.  **Download the Folder:** Get the **`lora_storygenie_weights`** folder from your Google Drive (where the Colab training saved them).

2.  **Placement:** Place the folder directly inside the `backend` directory:

    ```
    backend/
    ├── app/
    ├── venv/
    ├── lora_storygenie_weights/  <-- PLACE DOWNLOADED FOLDER HERE
    └── requirements.txt
    ```

-----

## ▶️ Running and Verification

### Start the Server

Start the FastAPI server from the `backend` directory. The application will automatically detect and load the fine-tuned weights.

```bash
(venv) $ uvicorn app.main:app --reload
```

### Verification

On successful startup, the console logs will confirm the specialized model is active:

```log
✅ Connected to MongoDB
💾 Found LoRA weights at ./lora_storygenie_weights. Applying fine-tuning...
✅ LoRA weights merged into model successfully.
INFO:      Application startup complete.
```

-----

## 🌐 API Endpoints

Access the full documentation and interactive interface at `http://127.0.0.1:8000/docs`.

### Example Generation Payload (Hindi)

Send a POST request to `/api/v1/stories/generate` with the following JSON structure:

```json
{
  "prompt": "एक पुराने कबाड़ी की दुकान में एक जादुई चाय की केतली मिलती है, जो हर बार चाय उबलने पर एक इच्छा पूरी करती है, लेकिन हर इच्छा में एक मज़ेदार गड़बड़ी हो जाती है।",
  "genre": "fantasy",
  "language": "hi",
  "length": "medium",
  "tone": "light_hearted"
}
```
