import os
from pydub import AudioSegment
import logging
import tempfile
import math  # Import math for ceil function

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def merge_audio(
    music_path: str, sfx_paths: list[str], loop_sfx: bool = True
) -> str | None:
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

                sfx_to_overlay: AudioSegment  # Define type hint

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
                    logging.warning(
                        f"SFX to overlay for {sfx_path} was unexpectedly None. Skipping overlay."
                    )

            except Exception as e:
                logging.error(f"Error processing sound effect {sfx_path}: {e}")
                continue  # Continue with the next SFX

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


def overlay_voice(base_audio_path: str, voice_audio_path: str) -> str | None:
    """
    Overlays a voice track onto a base audio track.
    The voice track is truncated if it is longer than the base audio.
    Always returns a path to a *new* temporary file, even if overlay is skipped.

    Args:
        base_audio_path: Path to the base audio file (e.g., merged music+sfx).
        voice_audio_path: Path to the voice audio file (e.g., generated TTS).

    Returns:
        Path to the new temporary merged audio file, or None if an error occurs.
    """
    final_audio = None
    try:
        logging.info(f"Loading base audio for voice overlay: {base_audio_path}")
        base_audio = AudioSegment.from_mp3(base_audio_path)
        base_duration_ms = len(base_audio)
        logging.info(f"Base audio duration: {base_duration_ms / 1000:.2f} seconds")

        logging.info(f"Loading voice audio for overlay: {voice_audio_path}")
        voice_audio = AudioSegment.from_mp3(voice_audio_path)
        voice_duration_ms = len(voice_audio)
        logging.info(f"Voice audio duration: {voice_duration_ms / 1000:.2f} seconds")

        if voice_duration_ms == 0:
            logging.warning("Voice audio has zero duration. Skipping overlay.")
            # Use the base audio as the final audio directly
            final_audio = base_audio
        else:
            # Determine the voice segment to overlay
            if voice_duration_ms > base_duration_ms:
                logging.warning(
                    "Voice audio is longer than base audio. Truncating voice."
                )
                voice_to_overlay = voice_audio[:base_duration_ms]
            else:
                voice_to_overlay = voice_audio

            # Overlay the voice onto the base audio
            logging.info("Overlaying voice onto base audio.")
            final_audio = base_audio.overlay(voice_to_overlay, position=0)

        # Export the final audio (either base or overlaid) to a new temporary file
        if final_audio:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp_file:
                final_filename = tmp_file.name
                logging.info(
                    f"Exporting final audio with voice overlay to: {final_filename}"
                )
                final_audio.export(final_filename, format="mp3")
                logging.info("Final audio export complete.")
                return final_filename
        else:
            # Should not happen if logic above is correct, but as a safeguard
            logging.error("Final audio object was unexpectedly None before export.")
            return None

    except FileNotFoundError as e:
        logging.error(f"Audio file not found during voice overlay: {e}")
        return None
    except Exception as e:
        logging.error(f"An error occurred during voice overlay: {e}")
        return None
