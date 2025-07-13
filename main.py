#!/usr/bin/env python3

import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

from config import MODEL_NAME, SYSTEM_PROMPT
from call_function import available_functions, execute_function_calls


def parse_args(args: str) -> tuple[str, bool]:
    print_verbose = False
    if "--help" in args or "-?" in args:
        print('''
AI Coding Agent
This agent uses the Google GenAI API to assist with development.

USAGE: python main.py "<PROMPT>" [--verbose]
EXAMPLE: python main.py "Fix formatting in print_info() in file pgk/data_reader.py" --verbose

The Agent can use function calls to:
- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

Relative filepaths are supported within the working directory.
''')
        return None, None

    if len(args) <= 1 or type(args[1]) is not str:
        print('AI Coding Agent\nUSAGE: python ./main.py "<PROMPT>" [--verbose]')
        return None, None
    if len(args) == 3:
        if args[2] == "--verbose":
            print_verbose = True
        else:
            print("ERROR: Unknown argument.")
            return None, None
    if len(args) > 3:
        print("ERROR: Too many arguments! Make sure to enclose prompt in quotation marks.")
        return None, None

    return args[1], print_verbose

def init_genai_client() -> genai.Client:
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    return client

def generate_response(client: genai.Client, user_prompt: str, verbose: bool) -> types.GenerateContentResponse:
    if verbose:
        print(f"User prompt: {user_prompt}\n")

    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)])
    ]

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions],
            system_instruction=SYSTEM_PROMPT)
    )

    return response

def process_response(response: types.GenerateContentResponse, verbose: bool) -> None:
    if response.function_calls is not None:
        try:
            execute_function_calls(response.function_calls, verbose)
        except RuntimeError as e:
            print(e)
            return
    elif response.text is not None:
        print(response.text)

    if verbose:
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

def main(args: str) -> int:
    user_prompt, print_verbose = parse_args(args)
    if user_prompt is None:
        return 1

    client = init_genai_client()
    response = generate_response(client, user_prompt, print_verbose)

    process_response(response, print_verbose)

    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv))

