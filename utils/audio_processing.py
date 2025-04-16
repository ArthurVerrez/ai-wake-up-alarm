import os
from pydub import AudioSegment
import logging
import tempfile
import math # Import math for ceil function

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def merge_audio(music_path: str, sfx_paths: list[str], loop_sfx: bool = True) -> str | None:
    """
    Merges sound effects onto a base music track.
    If a sound effect is shorter than the music and loop_sfx is True, it will be looped.
    If a sound effect is longer, it will be truncated.

    Args:
        music_path: Path to the background music file.
        sfx_paths: List of paths to the sound effect files.
        loop_sfx: If True, loop shorter sound effects to match music duration.
                  Defaults to True.

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

                # Prepare the sound effect segment (loop, truncate, or use as is)
                if sfx_duration_ms == 0:
                     logging.warning(f"Skipping zero-duration SFX: {sfx_path}")
                     continue

                sfx_to_overlay: AudioSegment # Define type hint

                if sfx_duration_ms < music_duration_ms:
                    if loop_sfx:
                        # Loop the SFX if it's shorter and looping is enabled
                        num_repeats = math.ceil(music_duration_ms / sfx_duration_ms)
                        logging.info(f"Looping SFX {sfx_path} {num_repeats} times.")
                        looped_sfx = sfx * num_repeats
                        # Truncate the looped SFX to match the music duration exactly
                        sfx_to_overlay = looped_sfx[:music_duration_ms]
                    else:
                        # Use the SFX as is (will play once at the beginning)
                        logging.info(f"Using short SFX {sfx_path} without looping.")
                        sfx_to_overlay = sfx
                elif sfx_duration_ms > music_duration_ms:
                    # Truncate the SFX if it's longer than the music
                    logging.warning(f"Truncating SFX {sfx_path} to music duration.")
                    sfx_to_overlay = sfx[:music_duration_ms]
                else:
                    # SFX duration matches music duration
                    sfx_to_overlay = sfx

                # Overlay the prepared sound effect onto the music track
                logging.info(f"Overlaying SFX: {sfx_path}")
                # Ensure sfx_to_overlay is not None before overlaying
                if sfx_to_overlay:
                     output_audio = output_audio.overlay(sfx_to_overlay, position=0)
                else:
                     # This case should technically not be reached with current logic
                     # but adding safety log
                     logging.warning(f"SFX to overlay for {sfx_path} was unexpectedly None. Skipping overlay.")

            except Exception as e:
                logging.error(f"Error processing sound effect {sfx_path}: {e}")
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