import streamlit as st
import config
from utils.audio_processing import merge_audio, overlay_voice
from utils.text_generation import generate_wake_up_message
from utils.tts_generation import generate_tts_audio
import os


def body():
    """Displays the main body content with selection forms and generation."""

    # Initialize session state
    if "generated_wake_up_text" not in st.session_state:
        st.session_state["generated_wake_up_text"] = config.DEFAULT_WAKE_UP_SCRIPT
    # Initialize selected voice ID if it doesn't exist (using the first voice as default)
    if "selected_voice_id" not in st.session_state:
        if config.ELEVENLABS_VOICES:
            st.session_state["selected_voice_id"] = config.ELEVENLABS_VOICES[0]["id"]
        else:
            st.session_state["selected_voice_id"] = None  # Handle case with no voices

    st.header("1. Create Your Wake-Up Message")

    # Change text_area to text_input for user description
    user_description = st.text_input(
        "Describe yourself (e.g., name, location, job, hobbies):",
        key="user_desc",
        placeholder="Example: My name is Alex, I live in London and work as a writer.",
        help="Provide details for a personalized message.",
    )

    if st.button("✨ Auto-generate Script", key="generate_text_button"):
        if user_description:
            with st.spinner("Generating your personalized script..."):
                generated_text = generate_wake_up_message(user_description)
                if generated_text and not generated_text.startswith("Error:"):
                    st.session_state["generated_wake_up_text"] = generated_text
                elif generated_text:
                    st.error(generated_text)
                else:
                    st.error("Failed to generate script. Unknown error.")
        else:
            st.warning("Please enter a description first.")

    # Text area to display/edit the generated script (initial value is now the default)
    st.session_state["generated_wake_up_text"] = st.text_area(
        "Your wake-up script (edit if needed):",
        value=st.session_state["generated_wake_up_text"],
        height=150,
        key="wake_up_script",
    )

    st.divider()

    # --- NEW SECTION: Voice Selection ---
    st.header("2. Select Voice")

    voice_options = {
        voice["id"]: f"{voice['name']} ({voice['description']})"
        for voice in config.ELEVENLABS_VOICES
    }

    # Function to update selected voice ID in session state
    def update_selected_voice():
        st.session_state.selected_voice_id = st.session_state.voice_select_key

    selected_voice_id = st.selectbox(
        "Choose a voice for your message:",
        options=list(voice_options.keys()),
        format_func=lambda voice_id: voice_options.get(voice_id, "Unknown Voice"),
        key="voice_select_key",  # Use a distinct key
        index=(
            list(voice_options.keys()).index(st.session_state.selected_voice_id)
            if st.session_state.selected_voice_id in voice_options
            else 0
        ),
        on_change=update_selected_voice,  # Update state on change
    )

    # Find the full details of the selected voice
    selected_voice_details = next(
        (
            v
            for v in config.ELEVENLABS_VOICES
            if v["id"] == st.session_state.selected_voice_id
        ),
        None,
    )

    if selected_voice_details:
        st.write(
            f"**Previewing:** {selected_voice_details['name']} - *{selected_voice_details['description']}*"
        )
        # Check if preview file exists before trying to play
        if os.path.exists(selected_voice_details["preview_file"]):
            st.audio(
                selected_voice_details["preview_file"], format="audio/mp3", start_time=0
            )
        else:
            st.warning(
                f"Preview audio not found for {selected_voice_details['name']} at {selected_voice_details['preview_file']}"
            )
    else:
        st.error("Selected voice details not found. Please check configuration.")

    with st.expander("Preview all available voices"):
        if not config.ELEVENLABS_VOICES:
            st.write("No voices configured.")
        else:
            for voice in config.ELEVENLABS_VOICES:
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

    st.header("5. Generate Your Final Alarm")  # Renumbered
    if st.button("Generate Alarm Sound", key="generate_button"):
        # Get selections
        final_script = st.session_state.get(
            "generated_wake_up_text", config.DEFAULT_WAKE_UP_SCRIPT
        )
        selected_voice_id = st.session_state.get("selected_voice_id")
        # selected_music_name is already defined above
        # selected_sfx_names is already defined above

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

            try:
                # 1. Generate TTS
                with st.spinner("Generating voice audio..."):
                    voice_details = next(
                        (
                            v
                            for v in config.ELEVENLABS_VOICES
                            if v["id"] == selected_voice_id
                        ),
                        None,
                    )
                    voice_settings = (
                        voice_details.get("voice_settings") if voice_details else None
                    )  # Use specific or default settings

                    generated_tts_path = generate_tts_audio(
                        final_script, selected_voice_id, voice_settings
                    )
                    if generated_tts_path:
                        temp_files_to_clean.append(generated_tts_path)
                        st.success("Voice audio generated.")
                    else:
                        st.error("Failed to generate voice audio.")
                        error_occurred = True

                # 2. Merge Music and SFX (only if TTS succeeded)
                merged_music_sfx_path = None
                if not error_occurred:
                    with st.spinner("Mixing background music and sound effects..."):
                        music_path = config.DEFAULT_MUSIC[selected_music_name]
                        sfx_paths = [
                            config.DEFAULT_SOUND_EFFECTS[name]
                            for name in selected_sfx_names
                        ]
                        merged_music_sfx_path = merge_audio(
                            music_path, sfx_paths, loop_sfx=True
                        )
                        if merged_music_sfx_path:
                            temp_files_to_clean.append(merged_music_sfx_path)
                            st.success("Background audio mixed.")
                        else:
                            st.error("Failed to mix background audio.")
                            error_occurred = True

                # 3. Overlay Voice onto Merged Background (only if both above succeeded)
                if not error_occurred and generated_tts_path and merged_music_sfx_path:
                    with st.spinner("Overlaying voice onto background..."):
                        final_alarm_path = overlay_voice(
                            merged_music_sfx_path, generated_tts_path
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
