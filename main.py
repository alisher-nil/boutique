import os
import sys

from dotenv import load_dotenv
from google.genai import Client
from google.genai.types import Content, GenerateContentConfig, Part

from functions import available_functions, call_function
from prompts import system_prompt

load_dotenv()

api_key: str | None = os.environ.get("GEMINI_API_KEY")
client = Client(api_key=api_key)
model_name = "gemini-2.0-flash-001"


def main():
    prompt, verbose = parse_args()
    agent_run(prompt, verbose)


def parse_args() -> tuple[str, bool]:
    args = set(sys.argv[1:])
    verbose_key = "--verbose"
    verbose = False
    if verbose_key in args:
        args.discard(verbose_key)
        verbose = True
    if len(args) != 1:
        print_instructions()
        sys.exit(1)
    prompt = args.pop()
    return prompt, verbose


def print_instructions() -> None:
    print("AI Code Assistant")
    print('\nUsage: uv run main.py "your prompt here" [--verbose]')
    print('Example: uv run main.py "How do I fix the calculator?"')


def agent_run(prompt: str, verbose: bool = False) -> None:
    if not prompt:
        return
    if verbose:
        print(f"User prompt: {prompt}")

    messages: list[Content] = [Content(role="user", parts=[Part(text=prompt)])]
    call_count_limit = 20
    call_count = 0

    while call_count < call_count_limit:
        try:
            result = generate_content(messages, verbose)
        except Exception as e:
            print(f"{'':-^40}")
            print(e)
            return
        if result:
            print(f"{'':-^40}")
            print(result)
            return
        call_count += 1
    print(f"{'':-^40}")
    print("Reached max iterations limit, exiting")


def generate_content(messages: list[Content], verbose: bool) -> str | None:
    response = client.models.generate_content(
        model=model_name,
        contents=messages,
        config=GenerateContentConfig(
            tools=[available_functions],
            system_instruction=system_prompt,
        ),
    )
    if verbose and response.usage_metadata:
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

    if not response.function_calls:
        return response.text

    if response.candidates:
        for candidate in response.candidates:
            # if verbose:
            for part in candidate.content.parts:
                if part.text:
                    print(f"{'':-^40}\n{part.text}\n{'':-^40}")
            messages.append(candidate.content)

    function_responses = []

    for function_call_part in response.function_calls:
        function_call_result = call_function(function_call_part, verbose)

        if not function_call_result.parts:
            raise Exception("Empty function call result")
        for response in function_call_result.parts:
            if not response.function_response:
                raise Exception("Empty function call result")
            if verbose:
                print(f"-> {response.function_response.response}\n")
            function_responses.append(response)

    if not function_responses:
        raise Exception("No function calls generated, exiting")

    messages.append(Content(role="tool", parts=function_responses))


if __name__ == "__main__":
    main()
