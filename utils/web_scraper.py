import httpx
from bs4 import BeautifulSoup
import logging

logger = logging.getLogger(__name__)

async def scrape_text_from_url(url: str) -> str | None:
    """
    Mengambil konten teks dari URL.
    """
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, timeout=15)
            response.raise_for_status() # Raise an exception for 4xx or 5xx status codes

        soup = BeautifulSoup(response.text, 'html.parser')

        # Hapus script dan style tags
        for script in soup(["script", "style"]):
            script.extract()

        # Dapatkan teks
        text = soup.get_text()

        # Pecah baris dan hapus spasi berlebih
        lines = (line.strip() for line in text.splitlines())
        # Gabungkan baris yang tidak kosong
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        # Filter baris kosong
        text = '\n'.join(chunk for chunk in chunks if chunk)

        logger.info(f"Berhasil scrape teks dari URL: {url}")
        return text

    except httpx.HTTPStatusError as e:
        logger.error(f"HTTP Error saat scrape URL {url}: {e.response.status_code} - {e.response.text}", exc_info=True)
        return None
    except httpx.RequestError as e:
        logger.error(f"Request Error saat scrape URL {url}: {e}", exc_info=True)
        return None
    except Exception as e:
        logger.error(f"Error tidak terduga saat scrape URL {url}: {e}", exc_info=True)
        return None
