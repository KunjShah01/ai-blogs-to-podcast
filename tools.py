import os
import tempfile
import trafilatura
from langchain_core.tools import tool
from elevenlabs import generate, save, set_api_key

# === ElevenLabs Setup ===
set_api_key("YOUR_ELEVENLABS_API_KEY")

# === Scraper Tool ===
@tool
def scrape_blog_content(url: str) -> str:
    """Scrape main blog content from URL."""
    downloaded = trafilatura.fetch_url(url)
    result = trafilatura.extract(downloaded)
    return result or "ERROR: Could not extract content."

# === TTS Tool ===
@tool
def generate_podcast_audio(text: str) -> str:
    """Convert podcast script to audio and return file path."""
    audio = generate(text=text, voice="Bella", model="eleven_multilingual_v2")
    temp_dir = tempfile.gettempdir()
    audio_path = os.path.join(temp_dir, "podcast_audio.mp3")
    save(audio, audio_path)
    return audio_path
