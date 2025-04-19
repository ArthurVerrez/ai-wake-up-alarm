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

# --- ElevenLabs Configuration ---
DEFAULT_VOICE_LEVEL = 100  # Default volume percentage (0-100)
VOICE_START_DELAY_MS = 3000  # Delay in milliseconds before voice starts
POST_VOICE_SILENCE_MS = 2000  # Silence duration after voice ends before fade
FADE_OUT_DURATION_MS = 3000  # Duration of the fade-out effect
DEFAULT_ELEVENLABS_MODEL_ID = "eleven_multilingual_v2"
DEFAULT_ELEVENLABS_OUTPUT_FORMAT = "mp3_44100_128"
DEFAULT_VOICE_SETTINGS = {
    "stability": 0.50,
    "similarity_boost": 0.95,
    "style": 0.5,
    "use_speaker_boost": True,
    "speed": 0.9,  # Default speed
}

ELEVENLABS_VOICES = [
    {
        # https://elevenlabs.io/app/voice-lab?voiceId=FA6HhUjVbervLw2rNl8M
        "id": "FA6HhUjVbervLw2rNl8M",
        "name": "Ophelia Rose",
        "description": "British Female, Soothing & Calm",
        "preview_file": "static/voices/FA6HhUjVbervLw2rNl8M.mp3",
        "voice_settings": DEFAULT_VOICE_SETTINGS,
    },
    {
        # https://elevenlabs.io/app/voice-lab?voiceId=FA6HhUjVbervLw2rNl8M
        "id": "KmnvDXRA0HU55Q0aqkPG",
        "name": "Australian Baritone",
        "description": "Soft, Slow & Calming",
        "preview_file": "static/voices/KmnvDXRA0HU55Q0aqkPG.mp3",
        "voice_settings": DEFAULT_VOICE_SETTINGS,
    },
    # Add more voices here in the future, ensuring preview files exist
    # Example for a future voice with custom settings:
    # {
    #     "id": "ANOTHER_VOICE_ID",
    #     "name": "Future Voice",
    #     "description": "Another description",
    #     "preview_file": "static/voices/ANOTHER_VOICE_ID.mp3",
    #     "voice_settings": {
    #         "stability": 0.60, # Custom setting
    #         "similarity_boost": 0.90,
    #         "style": 0.3,
    #         "use_speaker_boost": False,
    #         "speed": 1.0,
    #     }
    # },
]
# Ensure the 'static/voices/' directory exists and contains the preview MP3s named by ID.
