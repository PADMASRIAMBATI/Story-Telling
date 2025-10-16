# 📖 StoryGenie: AI-Powered Multilingual Storytelling Platform

**Repository Link:** `https://github.com/PADMASRIAMBATI/Story-Telling.git`

StoryGenie is a fully optimized **FastAPI backend** designed to generate high-quality, genre- and tone-specific fiction in **English, Hindi, and Telugu**. It utilizes a specialized, locally deployed Large Language Model (LLM) to ensure coherent and accurate narrative generation even on consumer hardware.

-----

## 🧠 Model & Fine-Tuning Overview

| Component | Detail | Description |
| :--- | :--- | :--- |
| **Core Model** | **Gemma 2-2B Instruct** | The small, efficient open-source model chosen for its stability and speed on local machines. |
| **Specialization** | **QLoRA Fine-Tuning** | The model was trained on a custom multilingual dataset to fix coherence and plot failures in Hindi/Telugu. |
| **Output Control** | **Few-Shot Prompting + $1.1$ Repetition Penalty** | Parameters are tuned to maximize the narrative flow and push stories closer to the requested 400–600 word length. |
| **Deployment** | **LoRA Adapter Merging** | The specialized weights are merged into the base model during startup, activating custom capabilities. |

-----

## 🏗️ Technical Stack

| Area | Technology | Role |
| :--- | :--- | :--- |
| **Backend API** | Python / **FastAPI** | High-performance, asynchronous RESTful interface. |
| **Frontend UI** | **React / JavaScript** | **The User Interface for interacting with the AI.** |
| **Data Storage** | MongoDB | Stores user profiles and story history. |

-----

## 🛠️ Full Project Deployment Guide

This guide ensures both the Python backend and the **React frontend** are launched correctly.

### A. Backend Setup (API and Model)

1.  **Clone and Initialize:**

    ```bash
    git clone https://github.com/PADMASRIAMBATI/Story-Telling.git
    cd Story-Telling/backend

    # Create and activate environment
    python -m venv venv
    source venv/bin/activate 
    ```

2.  **Install Python Dependencies:**

    ```bash
    (venv) $ pip install -r requirements.txt
    ```

3.  **Deploy Weights:** Place the downloaded **`lora_storygenie_weights`** folder directly inside the **`backend`** directory.

4.  **Start the Backend Server (API):**

    ```bash
    (venv) $ uvicorn app.main:app --reload
    ```

    *(The API will run on `http://127.0.0.1:8000`)*

### B. Frontend Setup (React UI)

**Open a NEW terminal window** and navigate to the frontend folder.

1.  **Navigate to Frontend Folder:**

    ```bash
    cd Story-Telling/frontend
    ```

2.  **Install Node Dependencies:**

    ```bash
    npm install
    ```

3.  **Start the React Application:**

    ```bash
    npm start
    ```

    *(The React app will open in your browser, typically at `http://localhost:3000`, connecting to the backend API you started in Step A.)*

-----

## 🌐 API Verification

With both the backend and frontend running, your React UI will communicate with your specialized AI model to generate high-quality, multilingual stories.
