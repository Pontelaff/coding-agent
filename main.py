#!/usr/bin/env python3

import os
import sys
from dotenv import load_dotenv
from google import genai

EXAMPLE_PROMT = "Tell me about yourself in 100 words or less"

def main() -> int:

    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)
    print('"' + EXAMPLE_PROMT + '"\n')
    response = client.models.generate_content(model="gemini-2.5-flash", contents=EXAMPLE_PROMT)

    print(response.text)

    print(f"\nPrompt tokens: {response.usage_metadata.prompt_token_count}")
    print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

    return 0

if __name__ == "__main__":
   sys.exit(main())

