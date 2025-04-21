APP_NAME = "AI Wake-Up Alarm Generator"
PAGE_TITLE = "AI Wake-Up Alarm Clock Generator"
PAGE_ICON = "🔔"
GITHUB_USERNAME = "ArthurVerrez"
GITHUB_REPOSITORY_NAME = "ai-wake-up-alarm"
GITHUB_REPOSITORY_LINK = (
    f"https://github.com/{GITHUB_USERNAME}/{GITHUB_REPOSITORY_NAME}"
)
CURRENT_VERSION = "0.0.1"


DEFAULT_SESSION_STATE = {
    # Add default session state variables here
    "example_session_attribute": "example_value",
}

QUICK_LINKS = [
    {
        "image": "static/images/gh_fav_logo.png",
        "link": GITHUB_REPOSITORY_LINK,
        "text": "Github Repository",
    },
    {
        "image": "static/images/st_fav_logo.png",
        "link": "https://streamlit.io/",
        "text": "Streamlit Documentation",
    },
]

# Default Audio Files
DEFAULT_SOUND_EFFECTS = {
    "Birds 1": "static/sound_effects/birds_1.mp3",
    "Rain": "static/sound_effects/rain.mp3",
    "Birds 2": "static/sound_effects/birds_2.mp3",
    "Car": "static/sound_effects/car.mp3",
}

DEFAULT_MUSIC = {
    "Spiritual 1": "static/music/spiritual_1.mp3",
    "Soft Synth": "static/music/soft_synth.mp3",
    "Soft Piano 3": "static/music/soft_piano_3.mp3",
    "Soft Piano 2": "static/music/soft_piano_2.mp3",
    "Soft Background Piano": "static/music/soft_background_piano.mp3",
    "Soft Guitar": "static/music/soft_guitar.mp3",
    "Calm": "static/music/calm.mp3",
}

# AI Configuration
OPENAI_MODEL_ID = "gpt-4.1-2025-04-14"
DEFAULT_WAKE_UP_SCRIPT = """Hey... Heyyy... good morning sleepyhead... it's time to wake up...
The sun is slowly rising on the horizon...
casting beautiful golden rays through your window...
Can you feel that gentle warmth?... The world is waking up with you...
Birds are starting their morning songs... The air is fresh and crisp...
Nature is stirring from its slumber... just like you...
Each breath you take fills you with renewed energy...
The morning dew sparkles like tiny diamonds on the grass...
A gentle breeze carries the sweet scent of dawn...
A brand new day full of endless possibilities is waiting just for you... Take your time...
no need to rush... stretch those sleepy muscles...
Feel the comfort of your cozy bed one last time...
Let your mind slowly drift into wakefulness... Like a flower opening to the morning light...
You're beginning to stir... The day ahead holds so much promise... so much potential...
Every morning is a fresh start... a new beginning... a chance to write your own story...
Your dreams from the night can become reality today... Rise and shine, beautiful soul...
The world is ready to embrace you... You're strong... you're capable...
you're ready for whatever comes your way... The day is yours to make amazing...
Each moment is a gift waiting to be unwrapped... Come on now... open those eyes...
Let's welcome this beautiful morning together... Take a deep breath...
feel the energy flowing through you... You're waking up exactly when you need to...
Everything is aligning perfectly for your day... Let's greet this wonderful morning together...
with hope in our hearts... and dreams in our minds..."""

# --- Sound Effect Configuration ---
DEFAULT_SFX_LEVEL = 75  # Default volume percentage (0-100)

# --- Music Configuration ---
DEFAULT_MUSIC_LEVEL = 65  # Default volume percentage (0-100)

# --- OpenAI TTS Configuration ---
OPENAI_TTS_MODEL_ID = "gpt-4o-mini-tts"  # Supports instructions
DEFAULT_VOICE_ID = "nova"
DEFAULT_VOICE_LEVEL = 100
VOICE_START_DELAY_MS = 3000
POST_VOICE_SILENCE_MS = 2000
FADE_OUT_DURATION_MS = 5000

# Detailed instructions for the TTS model (used with compatible models like gpt-4o-mini-tts)
OPENAI_TTS_INSTRUCTIONS = """Voice Affect: Ultra-soft, whispery, and nurturing; project extreme calm and safety, like a warm cocoon. Every word should feel like it's gently wrapping around the listener.

Tone: Subtly melodic and deeply reassuring, with a delicate British accent. Speak just above a murmur — never sharp, never rushed. Let the voice feel like it's gliding.

Pacing: Exceptionally slow and spacious; prioritize comfort over efficiency. Each sentence should have time to settle, inviting the listener to stay in the moment.

Emotion: Quietly affectionate, peaceful, and intimate — as if softly waking someone you love. Radiate gentle encouragement without urgency.

Pronunciation: Softened articulation; enunciate with breathy precision. Let important words like "calm," "safe," "ready," and "gently" land like feathers.

Pauses: Long, intentional silences between lines to allow the listener's awareness to drift into wakefulness. Use silence as part of the comfort."""

# Define available OpenAI voices
# (IDs must match OpenAI's 'voice' parameter options: alloy, echo, fable, onyx, nova, shimmer)
OPENAI_VOICES = [
    {
        "id": "nova",
        "name": "Nova",
        "description": "Female, Gentle & Soothing",
        "preview_file": "static/voices/nova_preview.mp3",
    },
    {
        "id": "onyx",
        "name": "Onyx",
        "description": "Male, Deep & Calming",
        "preview_file": "static/voices/onyx_preview.mp3",
    },
    # Add other voices (alloy, echo, fable, shimmer) here if desired
]
# Ensure the 'static/voices/' directory exists. Preview files need to be created manually.
