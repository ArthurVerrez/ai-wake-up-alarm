import os
from pydub import AudioSegment
import logging
import tempfile

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def merge_audio(music_path: str, sfx_paths: list[str]) -> str | None:
    """
    Merges sound effects onto a base music track.

    Args:
        music_path: Path to the background music file.
        sfx_paths: List of paths to the sound effect files.

    Returns:
        Path to the temporary merged audio file, or None if an error occurs.
    """
    try:
        logging.info(f"Loading music track: {music_path}")
        music = AudioSegment.from_mp3(music_path)
        output_audio = music
        music_duration_ms = len(music)
        logging.info(f"Music duration: {music_duration_ms / 1000:.2f} seconds")

        for sfx_path in sfx_paths:
            try:
                logging.info(f"Loading sound effect: {sfx_path}")
                sfx = AudioSegment.from_mp3(sfx_path)
                sfx_duration_ms = len(sfx)
                logging.info(f"SFX duration: {sfx_duration_ms / 1000:.2f} seconds")

                # If SFX is longer than music, truncate it
                if sfx_duration_ms > music_duration_ms:
                    logging.warning(f"Truncating SFX {sfx_path} to music duration.")
                    sfx = sfx[:music_duration_ms]

                # Overlay the sound effect onto the music track starting at the beginning
                logging.info(f"Overlaying SFX: {sfx_path}")
                output_audio = output_audio.overlay(sfx, position=0)

            except Exception as e:
                logging.error(f"Error processing sound effect {sfx_path}: {e}")
                # Optionally continue with other SFX or return None/raise error
                continue # Continue with the next SFX

        # Export the merged audio to a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp_file:
            output_filename = tmp_file.name
            logging.info(f"Exporting merged audio to: {output_filename}")
            output_audio.export(output_filename, format="mp3")
            logging.info("Export complete.")
            return output_filename

    except FileNotFoundError:
        logging.error(f"Music file not found: {music_path}")
        return None
    except Exception as e:
        logging.error(f"An error occurred during audio merging: {e}")
        return None 