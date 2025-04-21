# AI Wake-Up Alarm Generator 🔔

Create personalized wake-up alarms featuring a custom AI-generated voice message overlaid on your choice of background music and optional sound effects.

<img src="./example_usage.gif" alt="Example Usage" width="200"/>

**Example Alarm Output:**
[Listen to Example Alarm](https://gabalpha.github.io/read-audio/?p=https://raw.githubusercontent.com/ArthurVerrez/ai-wake-up-alarm/main/example_alarm.mp3)

## Quick Start / Example Usage

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/ArthurVerrez/ai-wake-up-alarm.git
    cd ai-wake-up-alarm
    ```
2.  **Set up environment:**
    - Ensure you have Python 3.10+ installed.
    - Create a virtual environment (recommended):
      ```bash
      python -m venv venv
      source venv/bin/activate  # On Windows use `venv\Scripts\activate`
      ```
    - Install dependencies:
      ```bash
      pip install -r requirements.txt
      ```
    - Install `ffmpeg` (required by `pydub`). Follow instructions for your OS: [https://ffmpeg.org/download.html](https://ffmpeg.org/download.html)
3.  **Configure API Keys:**
    - Create a `.env` file in the project root directory.
    - Add your API keys (OpenAI key is used for both text and speech):
      ```dotenv
      OPENAI_API_KEY="your_openai_api_key_here"
      # ELEVENLABS_API_KEY="your_elevenlabs_api_key_here" # No longer needed
      ```
4.  **Run the Streamlit app:**
    ```bash
    streamlit run app.py
    ```
5.  Open your browser to the local URL provided by Streamlit.
6.  Follow the steps in the app to create your alarm!

## Features

- **Personalized Script:** Generate a unique wake-up script (using OpenAI GPT-4).
- **Script Expansion:** Make the script longer.
- **Voice Selection:** Choose from multiple AI voices (powered by OpenAI TTS - e.g., Nova, Onyx).
- **Voice Preview:** (Requires manual creation of preview files).
- **Music Selection:** Choose a background music track.
- **Sound Effects:** Layer optional ambient sound effects (e.g., rain, birds).
- **Level Adjustment:** Fine-tune the volume levels for voice, music, and each sound effect individually.
- **Configurable Delays & Fade:** Control silence duration before the voice starts and add a fade-out at the end.
- **Download:** Download the final generated alarm sound as an MP3 file.

## Installation & Setup

Follow the steps in the [Quick Start](#quick-start--example-usage) section. Ensure `ffmpeg` is correctly installed and accessible in your system's PATH.

## Configuration

Most application settings can be modified in `config.py`:

- `APP_NAME`, `PAGE_TITLE`, `PAGE_ICON`: Basic Streamlit app metadata.
- `GITHUB_REPOSITORY_LINK`, etc.: Links used in the app.
- `DEFAULT_SOUND_EFFECTS`, `DEFAULT_MUSIC`: Dictionaries mapping display names to audio file paths within the `static/` directory.
- `OPENAI_MODEL_ID`: OpenAI model for script generation/expansion.
- `DEFAULT_WAKE_UP_SCRIPT`: The initial script shown in the text area.
- `DEFAULT_SFX_LEVEL`, `DEFAULT_MUSIC_LEVEL`, `DEFAULT_VOICE_LEVEL`: Default volume levels (0-100).
- `VOICE_START_DELAY_MS`: Silence before the voice starts.
- `POST_VOICE_SILENCE_MS`: Silence after the voice ends, before the fade-out.
- `FADE_OUT_DURATION_MS`: Duration of the final fade-out.
- `OPENAI_TTS_MODEL_ID`: OpenAI model for Text-to-Speech (e.g., `tts-1`).
- `DEFAULT_VOICE_ID`: Default OpenAI voice to use (e.g., `nova`).
- `OPENAI_VOICES`: List of available OpenAI voices. Each entry requires:
  - `id`: The OpenAI voice name (`alloy`, `echo`, `fable`, `onyx`, `nova`, `shimmer`).
  - `name`: Display name.
  - `description`: Short description.
  - `preview_file`: Path to a manually created preview MP3 (e.g., `static/voices/nova_preview.mp3`).

**API Keys:** Only the `OPENAI_API_KEY` is needed in the `.env` file.

## Adding New Audio/Voices

1.  **Music/Sound Effects:**
    - Place new MP3 files in the appropriate `static/music/` or `static/sound_effects/` directory.
    - Add a new entry to the `DEFAULT_MUSIC` or `DEFAULT_SOUND_EFFECTS` dictionary in `config.py`, mapping a user-friendly name to the file path.
2.  **Voices:**
    - Choose one of OpenAI's available voice IDs (`alloy`, `echo`, `fable`, `onyx`, `nova`, `shimmer`).
    - (Optional) Manually generate a short preview MP3 for the voice (e.g., using the OpenAI API directly or another tool).
    - Save the preview MP3 to `static/voices/` (e.g., `static/voices/shimmer_preview.mp3`).
    - Add a new dictionary entry to the `OPENAI_VOICES` list in `config.py`, filling in the `id`, `name`, `description`, and the `preview_file` path.

## Contributing ...

## License ...
