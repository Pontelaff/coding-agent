#!/usr/bin/env python3

import os
import sys
from dotenv import load_dotenv
from google import genai

def main(args) -> int:
    if len(args) <= 1:
        print("ERROR: Prompt is missing!")
        return 1
    if len(args) > 2:
        print("ERROR: Too many arguments! Make sure to enclose prompt in quotation marks.")
        return 1

    prompt = args[1]

    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)
    print('"' + prompt + '"\n')
    response = client.models.generate_content(model="gemini-2.0-flash", contents=prompt)

    print(response.text)

    print(f"\nPrompt tokens: {response.usage_metadata.prompt_token_count}")
    print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv))

