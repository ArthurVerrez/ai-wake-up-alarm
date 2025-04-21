import openai
import os
import logging
from dotenv import load_dotenv
import config

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

# Load environment variables (for API keys)
load_dotenv()

# Initialize OpenAI client
# It will automatically look for the OPENAI_API_KEY environment variable
try:
    client = openai.OpenAI()
    # Optionally test connection, e.g., list models if needed upon startup
    # client.models.list() # Uncomment to test API key on load
    logging.info("OpenAI client initialized successfully.")
except Exception as e:
    logging.error(f"Failed to initialize OpenAI client: {e}")
    client = None  # Set client to None if initialization fails


def generate_wake_up_message(user_description: str) -> str | None:
    """
    Generates a personalized wake-up message script using OpenAI.

    Args:
        user_description: A string containing details about the user
                          (name, location, job, likes, etc.).

    Returns:
        The generated wake-up message string, or None if an error occurs.
    """
    if not client:
        logging.error("OpenAI client not available. Cannot generate text.")
        return "Error: OpenAI client not configured. Check API key and logs."

    if not user_description:
        return "Please provide some details about yourself first."

    prompt = f"""
    Create a very gentle, slow, and soothing wake-up message script.
    It should sound like someone is softly trying to wake the person up.
    Start with 'Hey...' or 'Heyyy...' and use plenty of ellipses (...) 
    to indicate pauses and a slow pace. Keep sentences short and calm.

    Incorporate these details about the person being woken up:
    {user_description}

    The message should be positive and encouraging for the day ahead.
    Make it about 30 sentences long.
    Example of a beginning message: "Hey... Heyyy... [Name]... time to wake up sleepyhead... 
    The sun is shining in [Location]... another day for [Activity/Job] awaits... 
    Come on now... rise and shine..."

    Generated Script:
    """

    try:
        logging.info(
            f"Generating wake-up message for description: {user_description[:50]}..."
        )
        response = client.chat.completions.create(
            model=config.OPENAI_MODEL_ID,
            messages=[
                {
                    "role": "system",
                    "content": "You are a kind assistant creating gentle wake-up message scripts.",
                },
                {"role": "user", "content": prompt},
            ],
            temperature=0.7,  # Adjust for creativity vs. predictability
            max_tokens=500,  # Limit response length
        )
        generated_text = response.choices[0].message.content.strip()
        logging.info(f"Generated text: {generated_text}")
        return generated_text
    except Exception as e:
        logging.error(f"Error calling OpenAI API: {e}")
        return f"Error generating text: {e}"


def expand_wake_up_message(current_script: str) -> str | None:
    """
    Expands an existing wake-up message script using OpenAI, making it longer.

    Args:
        current_script: The existing wake-up script text.

    Returns:
        The expanded wake-up message string, or None if an error occurs.
    """
    if not client:
        logging.error("OpenAI client not available. Cannot expand text.")
        return "Error: OpenAI client not configured. Check API key and logs."

    if not current_script:
        return "There is no script to expand."

    prompt = f"""
    Take the following gentle, slow, and soothing wake-up message script 
    and make it approximately twice as long. 
    
    Maintain the existing gentle, slow pace, and soothing tone. 
    Use plenty of ellipses (...) for pauses. Keep sentences relatively short and calm.
    Add more encouraging words, gentle observations about the morning, 
    or soft prompts to wake up, weaving them naturally into the existing text.
    Do not drastically change the core message or style.
    
    Existing Script:
    --- --- ---
    {current_script}
    --- --- ---
    
    Expanded Script:
    """

    try:
        logging.info(
            f"Expanding wake-up message script starting with: {current_script[:50]}..."
        )
        response = client.chat.completions.create(
            model=config.OPENAI_MODEL_ID,  # Use the same model for consistency
            messages=[
                {
                    "role": "system",
                    "content": "You are a kind assistant expanding gentle wake-up message scripts.",
                },
                {"role": "user", "content": prompt},
            ],
            temperature=0.6,  # Slightly lower temp might be better for expansion
            max_tokens=500,  # Allow for a longer response
        )
        expanded_text = response.choices[0].message.content.strip()
        logging.info(f"Expanded text: {expanded_text}")
        return expanded_text
    except Exception as e:
        logging.error(f"Error calling OpenAI API for expansion: {e}")
        return f"Error expanding text: {e}"
