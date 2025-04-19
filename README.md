# AI Wake-Up Alarm Generator 🔔

Create personalized wake-up alarms featuring a custom AI-generated voice message overlaid on your choice of background music and optional sound effects.

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
    - Add your API keys:
      ```dotenv
      OPENAI_API_KEY="your_openai_api_key_here"
      ELEVENLABS_API_KEY="your_elevenlabs_api_key_here"
      ```
4.  **Run the Streamlit app:**
    ```bash
    streamlit run app.py
    ```
5.  Open your browser to the local URL provided by Streamlit.
6.  Follow the steps in the app to create your alarm!

## Features

- **Personalized Script:** Generate a unique wake-up script based on details you provide (using OpenAI GPT-4).
- **Script Expansion:** Make the generated script longer with a single click.
- **Voice Selection:** Choose from multiple AI voices (powered by ElevenLabs).
- **Voice Preview:** Listen to voice samples before selecting.
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
- `OPENAI_MODEL_ID`: The OpenAI model used for script generation/expansion.
- `DEFAULT_WAKE_UP_SCRIPT`: The initial script shown in the text area.
- `DEFAULT_SFX_LEVEL`, `DEFAULT_MUSIC_LEVEL`, `DEFAULT_VOICE_LEVEL`: Default volume levels (0-100).
- `VOICE_START_DELAY_MS`: Silence before the voice starts.
- `POST_VOICE_SILENCE_MS`: Silence after the voice ends, before the fade-out.
- `FADE_OUT_DURATION_MS`: Duration of the final fade-out.
- `DEFAULT_ELEVENLABS_MODEL_ID`, `DEFAULT_ELEVENLABS_OUTPUT_FORMAT`: Default settings for ElevenLabs API calls.
- `DEFAULT_VOICE_SETTINGS`: Default voice parameters (stability, speed, etc.) for ElevenLabs.
- `ELEVENLABS_VOICES`: List of available voices. Each entry requires:
  - `id`: The ElevenLabs Voice ID.
  - `name`: Display name.
  - `description`: Short description shown in the UI.
  - `preview_file`: Path (relative to project root) to a preview MP3 file (e.g., `static/voices/VOICE_ID.mp3`).
  - `voice_settings`: Specific voice settings dictionary for this voice (can use `DEFAULT_VOICE_SETTINGS`).

**API Keys:** As mentioned in setup, API keys for OpenAI and ElevenLabs **must** be placed in a `.env` file in the project root.

## Adding New Audio/Voices

1.  **Music/Sound Effects:**
    - Place new MP3 files in the appropriate `static/music/` or `static/sound_effects/` directory.
    - Add a new entry to the `DEFAULT_MUSIC` or `DEFAULT_SOUND_EFFECTS` dictionary in `config.py`, mapping a user-friendly name to the file path.
2.  **Voices:**
    - Find the Voice ID you want to use from your ElevenLabs Voice Lab.
    - Generate or find a short preview MP3 for the voice.
    - Save the preview MP3 to `static/voices/` and name it exactly `VOICE_ID.mp3`.
    - Add a new dictionary entry to the `ELEVENLABS_VOICES` list in `config.py`, filling in the `id`, `name`, `description`, `preview_file` path, and desired `voice_settings`.
