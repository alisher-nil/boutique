import os
import sys

from dotenv import load_dotenv
from google import genai

load_dotenv()

api_key: str | None = os.environ.get("GEMINI_API_KEY")
# model_name = "gemini-2.0-flash"
model_name = "gemini-2.0-flash-001"
client = genai.Client(api_key=api_key)


def main(prompt: str):
    if not prompt:
        return
    response = client.models.generate_content(model=model_name, contents=prompt)
    print(response.text)
    print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
    print(f"Response tokens: {response.usage_metadata.candidates_token_count}")


if __name__ == "__main__":
    args = sys.argv
    print(args)
    # main()
