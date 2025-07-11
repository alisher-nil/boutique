import os
import sys

from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()


api_key: str | None = os.environ.get("GEMINI_API_KEY")
model_name = "gemini-2.0-flash-001"
client = genai.Client(api_key=api_key)


def main(prompt: str, verbose: bool):
    if not prompt:
        return
    messages = [types.Content(role="user", parts=[types.Part(text=prompt)])]
    response = client.models.generate_content(model=model_name, contents=messages)
    print(response.text)

    if verbose:
        print(f"User prompt: {prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")


if __name__ == "__main__":
    args = set(sys.argv[1:])
    verbose_key = "--verbose"
    verbose = False
    if verbose_key in args:
        args.discard(verbose_key)
        verbose = True
    if len(args) != 1:
        print("Usage: uv run main.py 'prompt text'")
        sys.exit(1)
    main(args.pop(), verbose)
