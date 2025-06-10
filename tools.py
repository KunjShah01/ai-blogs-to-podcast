import os
import tempfile
import trafilatura
from langchain_core.tools import tool
from elevenlabs import text_to_speech

# === ElevenLabs Setup ===
eleven_api_key = os.getenv("ELEVEN_LABS_API_KEY")


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
    voice_id = "21m00Tcm4TlvDq8ikWAM"  # Bella voice ID
    audio = text_to_speech(
        text=text,
        voice=voice_id,
        model="eleven_multilingual_v2",
        api_key=eleven_api_key,
    )
    temp_dir = tempfile.gettempdir()
    audio_path = os.path.join(temp_dir, "podcast_audio.mp3")
    with open(audio_path, "wb") as f:
        f.write(audio)
    return audio_path
