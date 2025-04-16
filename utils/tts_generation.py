import os
import logging
import tempfile
from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs
import config
import io  # Import io for memory streams
from pydub import AudioSegment  # Import AudioSegment

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

# Load environment variables (for API keys)
load_dotenv()

# Initialize ElevenLabs client
try:
    eleven_client = ElevenLabs()
    # You might want to check if the API key is valid, e.g., by listing voices
    # eleven_client.voices.list()
    logging.info("ElevenLabs client initialized successfully.")
except Exception as e:
    logging.error(f"Failed to initialize ElevenLabs client: {e}")
    eleven_client = None


def generate_tts_audio(
    text: str, voice_id: str, voice_settings: dict | None = None
) -> str | None:
    """
    Generates TTS audio using the ElevenLabs API, adds leading silence,
    and saves it to a temporary file.

    Args:
        text: The text script to convert to speech.
        voice_id: The ID of the ElevenLabs voice to use.
        voice_settings: Optional dictionary of voice settings (stability, boost, etc.).
                        If None, uses defaults from config.

    Returns:
        Path to the temporary generated audio file (MP3 with leading silence),
        or None if an error occurs.
    """
    if not eleven_client:
        logging.error("ElevenLabs client not available. Cannot generate TTS.")
        return None

    if not text:
        logging.warning("No text provided for TTS generation.")
        return None

    effective_voice_settings = (
        voice_settings if voice_settings is not None else config.DEFAULT_VOICE_SETTINGS
    )

    try:
        logging.info(
            f'Generating TTS for text: "{text[:50]}..." using voice {voice_id}'
        )
        audio_stream = eleven_client.text_to_speech.convert(
            text=text,
            voice_id=voice_id,
            model_id=config.DEFAULT_ELEVENLABS_MODEL_ID,
            output_format=config.DEFAULT_ELEVENLABS_OUTPUT_FORMAT,
            voice_settings=effective_voice_settings,
        )

        # --- Process audio with pydub ---
        audio_bytes = b""
        for chunk in audio_stream:
            audio_bytes += chunk

        if not audio_bytes:
            logging.error("TTS generation resulted in empty audio data.")
            return None

        # Load generated audio into pydub
        tts_audio = AudioSegment.from_file(io.BytesIO(audio_bytes), format="mp3")

        # Create silence segment
        silence_duration = config.VOICE_START_DELAY_MS
        leading_silence = AudioSegment.silent(duration=silence_duration)

        # Concatenate silence + TTS audio
        final_tts_audio = leading_silence + tts_audio
        logging.info(f"Added {silence_duration}ms leading silence to TTS audio.")

        # Save the combined audio to a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp_file:
            output_filename = tmp_file.name
            logging.info(
                f"Saving TTS audio with silence to temporary file: {output_filename}"
            )
            final_tts_audio.export(output_filename, format="mp3")
            logging.info("TTS audio with silence saved successfully.")
            return output_filename

    except Exception as e:
        logging.error(f"Error during ElevenLabs TTS generation or processing: {e}")
        return None
