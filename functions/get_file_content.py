# get_file_content.py

import os
from google.genai import types

MAX_CHARACTERS = 10000

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Reads the content from a single file, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The filepath to read from, relative to the working directory.",
            ),
        },
    ),
)

def get_file_content(working_directory: str, file_path: str) -> str:
    working_directory_path = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))
    if not abs_file_path.startswith(working_directory_path):
        return f'Error: Cannot read "{os.path.basename(abs_file_path)}" as it is outside the permitted working directory'
    if not os.path.exists(abs_file_path) or not os.path.isfile(abs_file_path):
        return f'Error: File not found or is not a regular file: "{abs_file_path}"'

    with open(abs_file_path, "r") as file:
        if file is None:
            return f'Error: could not read file: "{os.path.basename(abs_file_path)}"'
        file_content = file.read(MAX_CHARACTERS)

    if os.path.getsize(abs_file_path) > MAX_CHARACTERS:
        file_content += f'\n[...File "{os.path.basename(abs_file_path)}" truncated at 10000 characters]'

    return file_content