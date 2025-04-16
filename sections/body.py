import streamlit as st
import config
from utils.audio_processing import merge_audio
import os


def body():
    """Displays the main body content with selection forms and generation."""

    st.header("1. Choose Your Wake-Up Music")
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

    st.header("2. Add Sound Effects (Optional)")
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

    st.header("3. Generate Your Alarm")
    if st.button("Generate Alarm Sound", key="generate_button"):
        if selected_music_name:
            music_path = config.DEFAULT_MUSIC[selected_music_name]
            sfx_paths = [
                config.DEFAULT_SOUND_EFFECTS[name]
                for name in selected_sfx_names
            ]

            with st.spinner("Mixing your custom alarm sound..."):
                merged_audio_path = merge_audio(music_path, sfx_paths)

            if merged_audio_path:
                st.success("Your alarm sound is ready!")
                st.audio(merged_audio_path, format="audio/mp3", start_time=0)

                # Add download button
                try:
                    with open(merged_audio_path, "rb") as fp:
                        btn = st.download_button(
                            label="Download Alarm Sound",
                            data=fp,
                            file_name=f"alarm_{selected_music_name.replace(' ', '_')}.mp3",
                            mime="audio/mp3",
                        )
                except Exception as e:
                    st.error(f"Error preparing download: {e}")
                finally:
                    # Clean up the temporary file after processing
                    if os.path.exists(merged_audio_path):
                         try:
                            os.remove(merged_audio_path)
                            st.info("Temporary file cleaned up.") # Optional: inform user
                         except OSError as e:
                            st.warning(f"Could not remove temporary file {merged_audio_path}: {e}")

            else:
                st.error(
                    "Failed to generate the alarm sound. Please check the logs."
                )
        else:
            st.warning("Please select a music track first.")
