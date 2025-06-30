import requests
import os
import logging
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger(__name__)

SHRINKME_API_TOKEN = os.getenv("SHRINKME_API_TOKEN")

def generate_shrinkme_link(original_url):
    if not SHRINKME_API_TOKEN:
        logger.error("SHRINKME_API_TOKEN tidak diset. Tidak dapat membuat shortlink.")
        return None

    api_url = "https://shrinkme.io/api"
    params = {
        "api": SHRINKME_API_TOKEN,
        "url": original_url
    }
    try:
        response = requests.get(api_url, params=params, timeout=10) # Tambahkan timeout
        response.raise_for_status() # Akan raise HTTPStatusError untuk 4xx/5xx responses
        data = response.json()
        if data.get("status") == "success":
            logger.info(f"Shortlink berhasil dibuat untuk {original_url}")
            return data.get("shortenedUrl")
        else:
            error_message = data.get("message", "Pesan error tidak tersedia.")
            logger.error(f"ShrinkMe.io API error untuk URL {original_url}: {error_message}. Response: {data}")
            return None
    except requests.exceptions.HTTPStatusError as e:
        logger.error(f"HTTP Error dari ShrinkMe.io API: {e.response.status_code} - {e.response.text}", exc_info=True)
        return None
    except requests.exceptions.ConnectionError as e:
        logger.error(f"Koneksi ke ShrinkMe.io gagal: {e}", exc_info=True)
        return None
    except requests.exceptions.Timeout as e:
        logger.error(f"Permintaan ke ShrinkMe.io timeout: {e}", exc_info=True)
        return None
    except requests.exceptions.RequestException as e:
        logger.error(f"Error umum saat request ke ShrinkMe.io: {e}", exc_info=True)
        return None
    except ValueError: # JSONDecodeError
        logger.error(f"Gagal decode JSON dari respon ShrinkMe.io: {response.text}", exc_info=True)
        return None
    except Exception as e:
        logger.error(f"Error tidak terduga saat membuat shortlink: {e}", exc_info=True)
        return None

