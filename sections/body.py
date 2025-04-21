import streamlit as st
import config
from utils.audio_processing import merge_audio, overlay_voice
from utils.text_generation import generate_wake_up_message, expand_wake_up_message
from utils.tts_generation import generate_openai_tts_audio
import os
from pydub import AudioSegment


def body():
    """Displays the main body content with selection forms and generation."""

    # Initialize session state
    st.session_state.setdefault("generated_wake_up_text", config.DEFAULT_WAKE_UP_SCRIPT)
    st.session_state.setdefault("selected_voice_id", config.DEFAULT_VOICE_ID)
    st.session_state.setdefault("sfx_levels", {})
    st.session_state.setdefault(
        "voice_level", config.DEFAULT_VOICE_LEVEL
    )  # Add voice level state
    st.session_state.setdefault(
        "music_level", config.DEFAULT_MUSIC_LEVEL
    )  # Add music level state

    # --- Step 1: Create Message ---
    st.header("1. Create Your Wake-Up Message")
    user_description = st.text_input(
        "Describe yourself...",
        key="user_desc",
        placeholder="Example: My name is Alex...",
        help="...",
    )

    # --- Buttons Side-by-Side ---
    col1, col2 = st.columns(2)
    with col1:
        if st.button(
            "✨ Auto-generate Script",
            key="generate_text_button",
            use_container_width=True,
        ):
            if user_description:
                with st.spinner("Generating script..."):
                    generated_text = generate_wake_up_message(user_description)
                    if generated_text and not generated_text.startswith("Error:"):
                        st.session_state["generated_wake_up_text"] = generated_text
                    elif generated_text:
                        st.error(generated_text)
                    else:
                        st.error("Failed to generate script. Unknown error.")
            else:
                st.warning("Please enter a description first to generate a new script.")

    with col2:
        if st.button(
            "↔️ Expand Script", key="expand_text_button", use_container_width=True
        ):
            current_script = st.session_state.get("generated_wake_up_text", "")
            if current_script:
                with st.spinner("Expanding script..."):
                    expanded_text = expand_wake_up_message(current_script)
                    if expanded_text and not expanded_text.startswith("Error:"):
                        st.session_state["generated_wake_up_text"] = expanded_text
                    elif expanded_text:
                        st.error(expanded_text)
                    else:
                        st.error("Failed to expand script. Unknown error.")
            else:
                st.warning("There is no script in the text box to expand.")
    # -------------------------

    # Update current_script variable after potential button clicks
    current_script = st.session_state.get(
        "generated_wake_up_text", config.DEFAULT_WAKE_UP_SCRIPT
    )

    st.session_state["generated_wake_up_text"] = st.text_area(
        "Your wake-up script (edit if needed):",
        value=current_script,
        height=150,
        key="wake_up_script",
    )
    st.caption(f"Character count: {len(st.session_state['generated_wake_up_text'])}")
    st.divider()

    # --- NEW SECTION: Voice Selection ---
    st.header("2. Select Voice")

    # Use OPENAI_VOICES from config
    voice_options = {
        voice["id"]: f"{voice['name']} ({voice['description']})"
        for voice in config.OPENAI_VOICES
    }

    # Ensure default exists in options, or default to first if available
    default_index = 0
    if config.DEFAULT_VOICE_ID in voice_options:
        default_index = list(voice_options.keys()).index(config.DEFAULT_VOICE_ID)
    elif voice_options:
        st.session_state["selected_voice_id"] = list(voice_options.keys())[0]
    else:  # No voices configured
        st.session_state["selected_voice_id"] = None

    # Function to update selected voice ID in session state
    def update_selected_voice():
        st.session_state.selected_voice_id = st.session_state.voice_select_key

    selected_voice_id_from_state = st.session_state.get("selected_voice_id")

    st.selectbox(
        "Choose a voice for your message:",
        options=list(voice_options.keys()),
        format_func=lambda voice_id: voice_options.get(voice_id, "Unknown Voice"),
        key="voice_select_key",
        index=(
            list(voice_options.keys()).index(selected_voice_id_from_state)
            if selected_voice_id_from_state in voice_options
            else default_index
        ),
        on_change=update_selected_voice,
    )

    # Find the full details of the selected voice
    selected_voice_details = next(
        (
            v
            for v in config.OPENAI_VOICES
            if v["id"] == st.session_state.selected_voice_id
        ),
        None,
    )

    if selected_voice_details:
        st.write(
            f"**Previewing:** {selected_voice_details['name']} - *{selected_voice_details['description']}*"
        )
        if os.path.exists(selected_voice_details["preview_file"]):
            st.audio(
                selected_voice_details["preview_file"], format="audio/mp3", start_time=0
            )
        else:
            st.warning(
                f"Preview audio for OpenAI voice '{selected_voice_details['name']}' not found at {selected_voice_details['preview_file']}. Previews need to be created manually."
            )
    elif voice_options:  # Only error if voices exist but selection failed
        st.error("Selected voice details not found. Please check configuration.")

    with st.expander("Preview all available voices"):
        if not config.OPENAI_VOICES:
            st.write("No voices configured.")
        else:
            for voice in config.OPENAI_VOICES:
                st.write(f"**{voice['name']}**: {voice['description']}")
                if os.path.exists(voice["preview_file"]):
                    st.audio(voice["preview_file"], format="audio/mp3", start_time=0)
                else:
                    st.caption(f"(Preview audio not found at {voice['preview_file']})")
                st.markdown("---")  # Separator

    st.divider()

    # --- Renumbered Sections ---
    st.header("3. Choose Your Wake-Up Music")  # Renumbered
    music_options = list(config.DEFAULT_MUSIC.keys())
    selected_music_name = st.selectbox(
        "Select one music track:", options=music_options, index=0, key="music_select"
    )

    if selected_music_name:
        st.write(f"Previewing: {selected_music_name}")
        st.audio(
            config.DEFAULT_MUSIC[selected_music_name],
            format="audio/mp3",
            start_time=0,
        )

    with st.expander("Preview all music tracks"):
        st.write("All available music tracks:")
        for name, path in config.DEFAULT_MUSIC.items():
            st.caption(name)
            st.audio(path, format="audio/mp3", start_time=0)

    st.divider()

    st.header("4. Add Sound Effects (Optional)")  # Renumbered
    sfx_options = list(config.DEFAULT_SOUND_EFFECTS.keys())
    selected_sfx_names = st.multiselect(
        "Select sound effects to layer:", options=sfx_options, key="sfx_multi"
    )

    if selected_sfx_names:
        st.write("Previewing selected sound effects:")
        for name in selected_sfx_names:
            st.caption(name)
            st.audio(
                config.DEFAULT_SOUND_EFFECTS[name], format="audio/mp3", start_time=0
            )

    with st.expander("Preview all sound effects"):
        st.write("All available sound effects:")
        for name, path in config.DEFAULT_SOUND_EFFECTS.items():
            st.caption(name)
            st.audio(path, format="audio/mp3", start_time=0)

    st.divider()

    # --- Step 5: Adjust Audio Levels (Optional) ---
    st.header("5. Adjust Levels (Optional)")

    with st.expander("Fine-tune Volume Levels"):
        # --- Voice Level Slider ---
        st.write("Adjust the master volume level (0-100) for the generated voice:")
        st.session_state["voice_level"] = st.slider(
            label="Voice Volume Level",
            min_value=0,
            max_value=100,
            value=st.session_state["voice_level"],
            key="voice_level_slider_moved",
        )
        st.markdown("---")  # Separator
        # -------------------------

        # --- Music Level Slider ---
        st.write("Adjust the master volume level (0-100) for the background music:")
        st.session_state["music_level"] = st.slider(
            label="Music Volume Level",
            min_value=0,
            max_value=100,
            value=st.session_state["music_level"],
            key="music_level_slider_moved",
        )
        st.markdown("---")  # Separator
        # -----------------------------

        # --- SFX Level Sliders ---
        st.write("Adjust the volume level (0-100) for each selected sound effect:")
        if selected_sfx_names:  # Use variable from Step 4
            current_sfx_levels = st.session_state.setdefault("sfx_levels", {})
            updated_levels = {}
            for sfx_name in selected_sfx_names:
                level = st.slider(
                    f"Level for **{sfx_name}**",
                    0,
                    100,
                    current_sfx_levels.get(sfx_name, config.DEFAULT_SFX_LEVEL),
                    key=f"level_slider_{sfx_name}",
                )
                updated_levels[sfx_name] = level
            st.session_state["sfx_levels"] = updated_levels
            # Cleanup removed SFX levels
            sfx_names_to_remove = [
                name for name in current_sfx_levels if name not in selected_sfx_names
            ]
            for name in sfx_names_to_remove:
                del st.session_state["sfx_levels"][name]
        else:
            st.caption("(No sound effects currently selected in Step 4)")
        # -------------------------

    st.divider()

    st.header("6. Generate Your Final Alarm")  # Renumbered
    if st.button("Generate Alarm Sound", key="generate_button"):
        # Get selections including new levels
        final_script = st.session_state.get(
            "generated_wake_up_text", config.DEFAULT_WAKE_UP_SCRIPT
        )
        selected_voice_id = st.session_state.get("selected_voice_id")
        voice_level = st.session_state.get("voice_level", config.DEFAULT_VOICE_LEVEL)
        music_level = st.session_state.get("music_level", config.DEFAULT_MUSIC_LEVEL)
        selected_music_name = st.session_state.get("music_select")
        selected_sfx_names = st.session_state.get("sfx_multi", [])
        current_sfx_levels_names = st.session_state.get("sfx_levels", {})

        # --- Validation ---
        if not final_script:
            st.warning("Please generate or enter a wake-up script.")
        elif not selected_voice_id:
            st.warning("Please select a voice.")
        elif not selected_music_name:
            st.warning("Please select a music track.")
        else:
            # --- Processing ---
            temp_files_to_clean = []
            final_alarm_path = None
            error_occurred = False
            target_duration = None

            # Map SFX names/levels to paths/levels for the processing function
            sfx_levels_paths = {
                config.DEFAULT_SOUND_EFFECTS[name]: current_sfx_levels_names.get(
                    name, config.DEFAULT_SFX_LEVEL
                )
                for name in selected_sfx_names  # Iterate through *selected* names only
            }
            sfx_paths_selected = [
                config.DEFAULT_SOUND_EFFECTS[name] for name in selected_sfx_names
            ]

            try:
                # 1. Generate TTS
                generated_tts_path = None
                with st.spinner("Generating voice audio using OpenAI..."):
                    generated_tts_path = generate_openai_tts_audio(
                        final_script, selected_voice_id
                    )

                    if generated_tts_path:
                        temp_files_to_clean.append(generated_tts_path)
                        # --- Get TTS Duration ---
                        try:
                            tts_segment = AudioSegment.from_mp3(generated_tts_path)
                            target_duration = len(tts_segment)
                            st.success(
                                f"Voice audio generated (Duration: {target_duration / 1000:.2f}s)."
                            )
                        except Exception as e_dur:
                            st.error(
                                f"Generated voice audio, but failed to get duration: {e_dur}"
                            )
                            error_occurred = (
                                True  # Treat as error if we can't get duration
                            )
                        # ------------------------
                    else:
                        st.error("Failed to generate voice audio.")
                        error_occurred = True

                # 2. Merge Music and SFX (using target_duration)
                merged_music_sfx_path = None
                if (
                    not error_occurred and target_duration is not None
                ):  # Check if target_duration was set
                    with st.spinner(
                        f"Mixing background music and sound effects to match voice duration ({target_duration / 1000:.2f}s)..."
                    ):
                        music_path = config.DEFAULT_MUSIC[selected_music_name]
                        # Pass target_duration to merge_audio
                        merged_music_sfx_path = merge_audio(
                            music_path,
                            sfx_paths_selected,
                            sfx_levels_paths,
                            music_level,
                            loop_sfx=True,
                            target_duration_ms=target_duration,
                        )
                        if merged_music_sfx_path:
                            temp_files_to_clean.append(merged_music_sfx_path)
                            st.success("Background audio mixed.")
                        else:
                            st.error("Failed to mix background audio.")
                            error_occurred = True
                elif not error_occurred and target_duration is None:
                    st.error(
                        "Skipping background mix because voice duration could not be determined."
                    )
                    error_occurred = True  # Cannot proceed without target duration

                # 3. Overlay Voice onto Merged Background (only if both above succeeded)
                if not error_occurred and generated_tts_path and merged_music_sfx_path:
                    with st.spinner("Overlaying voice onto background..."):
                        final_alarm_path = overlay_voice(
                            merged_music_sfx_path, generated_tts_path, voice_level
                        )
                        if final_alarm_path:
                            temp_files_to_clean.append(final_alarm_path)
                            st.success("Voice overlay complete.")
                        else:
                            st.error("Failed to overlay voice.")
                            error_occurred = True

                # --- Display Result ---
                if final_alarm_path and not error_occurred:
                    st.success("Your final alarm sound is ready!")
                    st.audio(final_alarm_path, format="audio/mp3", start_time=0)
                    # Add download button
                    try:
                        with open(final_alarm_path, "rb") as fp:
                            btn = st.download_button(
                                label="Download Final Alarm",
                                data=fp,
                                file_name=f"final_alarm_{selected_music_name.replace(' ', '_')}.mp3",
                                mime="audio/mp3",
                            )
                    except Exception as e:
                        st.error(f"Error preparing download: {e}")
                else:
                    # Error message was already shown in the respective step
                    st.error(
                        "Alarm generation failed. Please check the steps above and logs."
                    )

            except Exception as e:
                st.error(f"An unexpected error occurred during generation: {e}")
                error_occurred = True  # Ensure cleanup happens
            finally:
                # --- Cleanup ---
                st.info(f"Cleaning up {len(temp_files_to_clean)} temporary files...")
                for file_path in temp_files_to_clean:
                    if os.path.exists(file_path):
                        try:
                            os.remove(file_path)
                        except OSError as e_rem:
                            st.warning(
                                f"Could not remove temporary file {file_path}: {e_rem}"
                            )
                st.info("Cleanup complete.")
