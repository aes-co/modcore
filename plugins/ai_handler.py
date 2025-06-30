import os
import httpx
import logging
import uuid
import shutil
import threading
from fastapi import FastAPI
from fastapi.responses import FileResponse
import uvicorn
import subprocess

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

TEMP_STORAGE = "/tmp/modcore_ai_responses"
os.makedirs(TEMP_STORAGE, exist_ok=True)

app = FastAPI()

@app.get("/temp/{file_id}")
async def get_temp_file(file_id: str):
    file_path = f"{TEMP_STORAGE}/{file_id}.txt"
    if os.path.exists(file_path):
        return FileResponse(file_path)
    return {"error": "File tidak ditemukan"}

def run_file_server():
    uvicorn.run(app, host="0.0.0.0", port=8000)

threading.Thread(target=run_file_server, daemon=True).start()

# ===== FUNGSI AI OPENROUTER =====
async def generate_ai_reply(prompt: str) -> str:
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        logger.warning("API Key OpenRouter kosong.")
        return "[Fitur AI tidak aktif]"

    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "mistralai/mistral-7b-instruct", # Model default untuk chat
        "messages": [
            {"role": "system", "content": "Jawab sopan, santai, pakai bahasa Indonesia."},
            {"role": "user", "content": prompt}
        ]
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(url, headers=headers, json=payload)
            if response.status_code == 200:
                hasil = response.json()['choices'][0]['message']['content'].strip()
                return hasil
            else:
                logger.error(f"Respon AI gagal: {response.text}")
                return f"[Gagal AI: {response.status_code}]"
    except Exception as e:
        logger.error(f"Error AI request: {e}")
        return f"[Error AI: {e}]"

# ===== FUNGSI AI LOKAL (Ollama) =====
def get_ai_local_response(question: str, ollama_model: str = "llama2") -> str:
    try:
        result = subprocess.run(
            ['ollama', 'chat', '--model', ollama_model, '--prompt', question],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE, # Tangkap stderr juga untuk debugging
            text=True # Pastikan output adalah string
        )
        if result.returncode != 0:
            logger.error(f"Ollama command failed with error: {result.stderr}")
            return f"[Error Ollama: {result.stderr.strip()}]"
        
        response = result.stdout.strip()
        return response if response else "[Jawaban kosong]"
    except FileNotFoundError:
        logger.error("Ollama command not found. Is Ollama installed and in PATH?")
        return "[Error: Ollama tidak ditemukan. Pastikan sudah terinstal dan di PATH.]"
    except Exception as e:
        logger.error(f"Gagal AI Lokal: {e}")
        return f"[Error AI Lokal: {e}]"

# ===== FUNGSI AI untuk Ringkasan Teks dan Generasi Pesan Kreatif - BARU =====
async def summarize_text_ai(text: str, ai_provider: str, ollama_model: str = "llama2") -> str:
    prompt = f"Ringkas teks berikut ini secara singkat dan padat dalam bahasa Indonesia:\n\n{text}"
    if ai_provider == "openrouter":
        return await generate_ai_reply(prompt)
    elif ai_provider == "ollama":
        return get_ai_local_response(prompt, ollama_model)
    else:
        return "[Fitur ringkasan AI tidak aktif atau provider tidak didukung.]"

async def generate_creative_message_ai(theme: str, ai_provider: str, ollama_model: str = "llama2") -> str:
    prompt = f"Buatkan pesan kreatif dan menarik dalam bahasa Indonesia dengan tema: {theme}. Gunakan gaya bahasa yang sopan dan santai."
    if ai_provider == "openrouter":
        return await generate_ai_reply(prompt)
    elif ai_provider == "ollama":
        return get_ai_local_response(prompt, ollama_model)
    else:
        return "[Fitur generasi pesan AI tidak aktif atau provider tidak didukung.]"
