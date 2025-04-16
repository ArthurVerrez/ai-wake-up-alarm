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
