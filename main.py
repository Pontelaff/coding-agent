#!/usr/bin/env python3

import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_files_info import get_files_info, schema_get_files_info
from functions.get_file_content import get_file_content, schema_get_file_content
from functions.write_file import write_file, schema_write_file
from functions.run_python_file import run_python_file, schema_run_python_file

MODEL_NAME = "gemini-2.0-flash"
SYSTEM_PROMPT = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.

Add a short response text describing the actions you took.
"""

def print_response(prompt: str, response: types.GenerateContentResponse, verbose: bool) -> None:
    if verbose:
        print(f"User prompt: {prompt}\n")
    if response.function_calls is not None:
        for call in response.function_calls:
            print(f"Calling function: {call.name}({call.args})")
    elif response.text is not None:
        print(response.text)
    if verbose:
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

def main(args: str) -> int:
    print_verbose = False
    if len(args) <= 1 or type(args[1]) is not str:
        print("ERROR: Prompt is missing!")
        return 1
    if len(args) == 3:
        if args[2] == "--verbose":
            print_verbose = True
        else:
            print("ERROR: Unknown argument.")
            return 1
    if len(args) > 3:
        print("ERROR: Too many arguments! Make sure to enclose prompt in quotation marks.")
        return 1

    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)
    user_prompt = args[1]
    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)])
    ]
    available_functions = types.Tool(
        function_declarations=[
            schema_get_files_info,
            schema_get_file_content,
            schema_write_file,
            schema_run_python_file,
        ]
    )

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions],
            system_instruction=SYSTEM_PROMPT)
    )

    print_response(user_prompt, response, print_verbose)

    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv))

