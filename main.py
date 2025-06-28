#!/usr/bin/env python3

import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

def main(args) -> int:
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

    prompt = args[1]
    messages = [
        types.Content(role="user", parts=[types.Part(text=prompt)])
    ]

    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)
    if print_verbose:
        print(f"User prompt: {prompt}\n")
    response = client.models.generate_content(model="gemini-2.0-flash", contents=messages)

    print(response.text)

    if print_verbose:
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv))

