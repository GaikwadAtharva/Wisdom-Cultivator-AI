import os

from dotenv import load_dotenv

from ibm_watsonx_ai import Credentials
from ibm_watsonx_ai.foundation_models import ModelInference
from ibm_watsonx_ai.metanames import GenTextParamsMetaNames as GenParams

load_dotenv()

API_KEY = os.getenv("IBM_API_KEY")
PROJECT_ID = os.getenv("PROJECT_ID")
URL = os.getenv("IBM_URL")

credentials = Credentials(api_key=API_KEY, url=URL)

parameters = {
    GenParams.MAX_NEW_TOKENS: 160,
    GenParams.TEMPERATURE: 0.6,
}

model = ModelInference(
    model_id="ibm/granite-4-h-small",
    credentials=credentials,
    project_id=PROJECT_ID,
    params=parameters,
)

SYSTEM_PROMPT = """
You are Wisdom Cultivator AI, a calm self-reflection companion.

Response rules:
- Keep responses short and meaningful.
- Use 1 to 2 short paragraphs.
- Help the user reflect instead of giving direct life decisions.
- Be supportive, calm, and non-judgmental.
- Avoid long lists unless the user asks.
- End with exactly one thoughtful reflection question.
"""


def get_granite_response(user_message):

    prompt = f"""
{SYSTEM_PROMPT}

Conversation:
{user_message}

Wisdom Cultivator AI:
"""

    response = model.generate_text(prompt=prompt)

    return response.strip()


def generate_reflection_title(first_message):

    prompt = f"""
Create a short reflection journal title from this message.

Rules:
- 3 to 5 words only.
- No quotes.
- No full stop.
- Make it clear and meaningful.

Message:
{first_message}

Title:
"""

    title = model.generate_text(prompt=prompt)

    return title.strip()