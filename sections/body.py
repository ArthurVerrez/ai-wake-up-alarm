import streamlit as st
import config


def body():
    """Displays the main body content with selection forms for audio."""

    st.header("Choose Your Wake-Up Music")
    music_options = list(config.DEFAULT_MUSIC.keys())
    selected_music_name = st.selectbox(
        "Select one music track:", options=music_options, index=0
    )

    if selected_music_name:
        st.write(f"Playing: {selected_music_name}")
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

    st.header("Add Sound Effects (Optional)")
    sfx_options = list(config.DEFAULT_SOUND_EFFECTS.keys())
    selected_sfx_names = st.multiselect(
        "Select sound effects to layer:", options=sfx_options
    )

    if selected_sfx_names:
        st.write("Selected sound effects:")
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
