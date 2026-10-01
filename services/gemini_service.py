import os

from dotenv import load_dotenv
from google import genai
from google.genai import types


load_dotenv()

api_key = os.getenv("google_apikey")

if not api_key:
    raise ValueError(
        "google_apikey anahtarını .env dosyasında tanımlayın."
    )


client = genai.Client(api_key=api_key)


def generate_text(
    prompt: str,
    temperature: float = 0.7,
    max_output_tokens: int = 1000
) -> str:

    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=prompt,
        config=types.GenerateContentConfig(
            temperature=temperature,
            max_output_tokens=max_output_tokens,
        ),
    )

    return response.text or ""

def safe_generate_text(
    prompt: str,
    temperature: float = 0.7,
    max_output_tokens: int = 1000
) -> str | None:

    try:

        response = generate_text(
            prompt,
            temperature=temperature,
            max_output_tokens=max_output_tokens
        )

        return response

    except Exception as e:

        print(f"Gemini API hatası: {e}")

        return None

