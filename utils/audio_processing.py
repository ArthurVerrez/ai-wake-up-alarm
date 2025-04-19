import os
from pydub import AudioSegment
import logging
import tempfile
import math  # Import math for ceil function
import config  # Ensure config is imported

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


# Helper function to convert level (0-100) to dB adjustment
def level_to_db(level: int) -> float:
    """Converts a 0-100 level to dB adjustment (-40dB to 0dB)."""
    if level <= 0:
        return -60.0  # Near silence for 0 or less
    # Simple linear mapping: 100 -> 0dB, 0 -> -40dB
    # (Could use logarithmic mapping for more perceptual linearity if needed)
    return (level - 100.0) * 0.4


def merge_audio(
    music_path: str,
    sfx_paths: list[str],
    sfx_levels: dict[str, int],
    music_level: int,
    loop_sfx: bool = True,
    target_duration_ms: int | None = None,
) -> str | None:
    """
    Merges music and sound effects, adjusting levels and duration.
    If target_duration_ms is provided, loops/truncates music and SFX to match it.
    Otherwise, uses the original music duration.

    Args:
        music_path: Path to the background music file.
        sfx_paths: List of paths to the sound effect files.
        sfx_levels: Dictionary mapping SFX path to its volume level (0-100).
        music_level: Volume level for the music track (0-100).
        loop_sfx: If True, loop shorter sound effects.
        target_duration_ms: The desired final duration in milliseconds. If None,
                            uses the original music duration.

    Returns:
        Path to the temporary merged audio file, or None if an error occurs.
    """
    try:
        logging.info(f"Loading music track: {music_path}")
        music = AudioSegment.from_mp3(music_path)
        music_original_duration_ms = len(music)

        # Determine the reference duration for processing
        if target_duration_ms is None:
            reference_duration_ms = music_original_duration_ms
            logging.info(
                f"Using original music duration as reference: {reference_duration_ms / 1000:.2f}s"
            )
        else:
            reference_duration_ms = target_duration_ms
            logging.info(
                f"Using target duration as reference: {reference_duration_ms / 1000:.2f}s"
            )

        # Apply Music Level
        music_db_adjustment = level_to_db(music_level)
        logging.info(
            f"Adjusting music volume by {music_db_adjustment:.2f} dB (Level: {music_level})"
        )
        adjusted_music = music + music_db_adjustment

        # --- Adjust Music Duration ---
        if len(adjusted_music) == 0:
            logging.warning("Adjusted music has zero duration. Skipping music track.")
            # Start with silence if music is empty
            output_audio = AudioSegment.silent(duration=reference_duration_ms)
        elif len(adjusted_music) < reference_duration_ms:
            logging.info(
                f"Looping music to match reference duration ({reference_duration_ms / 1000:.2f}s)."
            )
            num_repeats = math.ceil(reference_duration_ms / len(adjusted_music))
            output_audio = (adjusted_music * num_repeats)[:reference_duration_ms]
        elif len(adjusted_music) > reference_duration_ms:
            logging.info(
                f"Truncating music to match reference duration ({reference_duration_ms / 1000:.2f}s)."
            )
            output_audio = adjusted_music[:reference_duration_ms]
        else:
            output_audio = adjusted_music  # Duration matches
        # ---------------------------

        logging.info(
            f"Base audio initialized with duration: {len(output_audio) / 1000:.2f}s"
        )

        # Process and overlay SFX
        for sfx_path in sfx_paths:
            try:
                logging.info(f"Loading sound effect: {sfx_path}")
                sfx = AudioSegment.from_mp3(sfx_path)
                sfx_original_duration_ms = len(sfx)
                if sfx_original_duration_ms == 0:
                    continue

                # Apply SFX Level
                level = sfx_levels.get(sfx_path, config.DEFAULT_SFX_LEVEL)
                db_adjustment = level_to_db(level)
                logging.info(
                    f"Adjusting SFX {sfx_path} volume by {db_adjustment:.2f} dB (Level: {level})"
                )
                sfx_adjusted = sfx + db_adjustment
                sfx_to_process = sfx_adjusted
                sfx_current_duration_ms = len(sfx_to_process)

                # Adjust SFX Duration (loop/truncate to reference_duration_ms)
                sfx_to_overlay: AudioSegment
                if sfx_current_duration_ms < reference_duration_ms:
                    if loop_sfx:
                        num_repeats = math.ceil(
                            reference_duration_ms / sfx_current_duration_ms
                        )
                        logging.info(
                            f"Looping adjusted SFX {sfx_path} to reference duration ({reference_duration_ms/1000:.2f}s). Repeats: {num_repeats}"
                        )
                        looped_sfx = sfx_to_process * num_repeats
                        sfx_to_overlay = looped_sfx[:reference_duration_ms]
                    else:
                        logging.info(
                            f"Using short adjusted SFX {sfx_path} without looping."
                        )
                        sfx_to_overlay = (
                            sfx_to_process  # Will be overlaid only once at the start
                        )
                elif sfx_current_duration_ms > reference_duration_ms:
                    logging.warning(
                        f"Truncating adjusted SFX {sfx_path} to reference duration ({reference_duration_ms/1000:.2f}s)."
                    )
                    sfx_to_overlay = sfx_to_process[:reference_duration_ms]
                else:
                    sfx_to_overlay = sfx_to_process

                # Overlay onto output audio
                logging.info(f"Overlaying processed SFX: {sfx_path}")
                if sfx_to_overlay:
                    output_audio = output_audio.overlay(sfx_to_overlay, position=0)
                else:
                    logging.warning(
                        f"SFX to overlay for {sfx_path} was unexpectedly None."
                    )

            except Exception as e:
                logging.error(f"Error processing sound effect {sfx_path}: {e}")
                continue

        # Export the final merged background audio
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp_file:
            output_filename = tmp_file.name
            logging.info(
                f"Exporting merged background audio (duration: {len(output_audio)/1000:.2f}s) to: {output_filename}"
            )
            output_audio.export(output_filename, format="mp3")
            logging.info("Background merge export complete.")
            return output_filename

    except FileNotFoundError as e:
        logging.error(f"Music file not found in merge_audio: {e}")
        return None
    except Exception as e:
        logging.error(f"An error occurred during background merging: {e}")
        return None


def overlay_voice(
    base_audio_path: str, voice_audio_path: str, voice_level: int
) -> str | None:
    """
    Overlays a voice track (with adjusted volume) onto a base audio track.

    Args:
        base_audio_path: Path to the base audio file.
        voice_audio_path: Path to the voice audio file.
        voice_level: Volume level for the voice audio (0-100).

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
            logging.warning(
                "Voice audio has zero duration. Skipping overlay processing."
            )
            final_audio = base_audio  # Use base audio as is
        else:
            # --- Apply Voice Level ---
            voice_db_adjustment = level_to_db(voice_level)
            logging.info(
                f"Adjusting voice volume by {voice_db_adjustment:.2f} dB (Level: {voice_level})"
            )
            adjusted_voice = voice_audio + voice_db_adjustment
            # -----------------------

            voice_to_process = adjusted_voice
            voice_duration_ms = len(voice_to_process)

            if voice_duration_ms > base_duration_ms:
                logging.warning(
                    "Adjusted voice audio is longer than base audio. Truncating voice."
                )
                voice_to_overlay = voice_to_process[:base_duration_ms]
            else:
                voice_to_overlay = voice_to_process

            logging.info("Overlaying adjusted voice onto base audio.")
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
