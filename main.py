import os
import sys

from dotenv import load_dotenv
from google import genai
from google.genai import types

from functions import available_functions, call_function
from prompts import system_prompt

load_dotenv()

api_key: str | None = os.environ.get("GEMINI_API_KEY")
model_name = "gemini-2.0-flash-001"
client = genai.Client(api_key=api_key)


def main(prompt: str, verbose: bool = False):
    if not prompt:
        return

    while True:
        break

    messages: list[types.Content] = [
        types.Content(role="user", parts=[types.Part(text=prompt)])
    ]
    response = client.models.generate_content(
        model=model_name,
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions], system_instruction=system_prompt
        ),
    )

    if response.candidates:
        for candidate in response.candidates:
            messages.append(candidate.content)

    if verbose:
        print(f"User prompt: {prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")  # ty: ignore[possibly-unbound-attribute]
        print(
            "Response tokens: "
            f"{response.usage_metadata.candidates_token_count}"  # ty: ignore[possibly-unbound-attribute]
        )

    if response.function_calls:
        for function_call_part in response.function_calls:
            result = call_function(function_call_part, verbose)
            messages.append(result)
            if result.parts and result.parts[0].function_response.response:
                print(f"-> {result.parts[0].function_response.response}")
            else:
                raise Exception("Fatal error: nothing returned from func call")
    else:
        print(response.text)


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
