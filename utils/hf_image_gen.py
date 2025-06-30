import httpx
import os
import logging

logger = logging.getLogger(__name__)

# Ambil token dari environment variable
HF_API_TOKEN = os.getenv("HF_API_TOKEN")

# Ganti dengan URL API Inference untuk model Stable Diffusion pilihan Anda
# Anda bisa menemukan model di Hugging Face Hub (https://huggingface.co/models?pipeline_tag=text-to-image)
# Contoh: stabilityai/stable-diffusion-xl-base-1.0
# Pastikan model yang Anda pilih mendukung Inference API dan memiliki kualitas yang baik.
HF_IMAGE_GEN_API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"

async def generate_image_hf(prompt: str) -> bytes | None:
    if not HF_API_TOKEN:
        logger.error("HF_API_TOKEN tidak diset. Tidak dapat memanggil Hugging Face API.")
        return None

    headers = {"Authorization": f"Bearer {HF_API_TOKEN}"}
    payload = {"inputs": prompt}

    try:
        async with httpx.AsyncClient() as client:
            # Timeout lebih lama karena generasi gambar bisa memakan waktu
            response = await client.post(HF_IMAGE_GEN_API_URL, headers=headers, json=payload, timeout=120)
            response.raise_for_status() # Akan raise HTTPStatusError untuk 4xx/5xx responses
            
            # Hugging Face Inference API untuk text-to-image biasanya mengembalikan byte gambar langsung
            return response.content
    except httpx.HTTPStatusError as e:
        logger.error(f"HTTP Error dari Hugging Face Image Gen: {e.response.status_code} - {e.response.text}", exc_info=True)
        if e.response.status_code == 503: # Service Unavailable, sering terjadi jika model sedang dimuat
            logger.error("Model Hugging Face mungkin sedang dimuat atau tidak tersedia. Coba lagi.")
        return None
    except httpx.RequestError as e:
        logger.error(f"Request Error ke Hugging Face Image Gen: {e}", exc_info=True)
        return None
    except Exception as e:
        logger.error(f"Error tidak terduga saat memanggil Hugging Face Image Gen: {e}", exc_info=True)
        return None
