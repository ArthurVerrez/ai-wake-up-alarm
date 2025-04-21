import os
import logging
import tempfile
import config
import io
from pydub import AudioSegment

# Reuse the OpenAI client from text_generation utils
from utils.text_generation import client as openai_client

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def generate_openai_tts_audio(text: str, voice_id: str) -> str | None:
    """
    Generates TTS audio using the OpenAI API (with instructions from config),
    adds leading silence, and saves it to a temporary file.

    Args:
        text: The text script to convert to speech.
        voice_id: The ID of the OpenAI voice to use (e.g., 'nova', 'onyx').

    Returns:
        Path to the temporary generated audio file (MP3 with leading silence),
        or None if an error occurs.
    """
    if not openai_client:
        logging.error("OpenAI client not available. Cannot generate TTS.")
        return None
    if not text:
        logging.warning("No text provided for TTS generation.")
        return None
    if not voice_id:
        logging.warning("No voice_id provided for TTS generation.")
        return None

    try:
        logging.info(
            f'Generating OpenAI TTS for text: "{text[:50]}..." using voice {voice_id} with instructions.'
        )

        # Use the synchronous client's method, adding instructions from config
        response = openai_client.audio.speech.create(
            model=config.OPENAI_TTS_MODEL_ID,
            voice=voice_id,
            input=text,
            instructions=config.OPENAI_TTS_INSTRUCTIONS,
            response_format="mp3",  # Request MP3 format for pydub compatibility
        )

        # Read the audio content bytes
        audio_bytes = response.read()

        if not audio_bytes:
            logging.error("OpenAI TTS generation resulted in empty audio data.")
            return None

        # Load generated audio into pydub
        tts_audio = AudioSegment.from_file(io.BytesIO(audio_bytes), format="mp3")

        # Create silence segment
        silence_duration = config.VOICE_START_DELAY_MS
        leading_silence = AudioSegment.silent(duration=silence_duration)

        # Concatenate silence + TTS audio
        final_tts_audio = leading_silence + tts_audio
        logging.info(f"Added {silence_duration}ms leading silence to OpenAI TTS audio.")

        # Save the combined audio to a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp_file:
            output_filename = tmp_file.name
            logging.info(
                f"Saving OpenAI TTS audio with silence to temporary file: {output_filename}"
            )
            final_tts_audio.export(output_filename, format="mp3", bitrate="192k")
            logging.info("OpenAI TTS audio with silence saved successfully.")
            return output_filename

    except Exception as e:
        logging.error(f"Error during OpenAI TTS generation or processing: {e}")
        # Attempt to log more details from OpenAI error if possible
        if hasattr(e, "response") and hasattr(e.response, "text"):
            logging.error(f"OpenAI API Error Response: {e.response.text}")
        elif hasattr(e, "body"):  # Newer openai versions might have body
            logging.error(f"OpenAI API Error Body: {e.body}")
        return None
