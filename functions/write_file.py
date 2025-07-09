# write_file.py

import os
from google.genai import types

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Write contents to the specified file path, constrained to the working directory. Create file if it doesn't exist, overwrite otherwise.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path to write to, relative to the working directory.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content to write to the file.",
            ),
        },
    ),
)

def write_file(working_directory: str, file_path: str, content: str) -> str:
    working_directory_path = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))

    if not abs_file_path.startswith(working_directory_path):
        return f'Error: Cannot write to "{os.path.basename(abs_file_path)}" as it is outside the permitted working directory'
    if os.path.exists(abs_file_path) and not os.path.isfile(abs_file_path):
        return f'Error: File is not a regular file: "{os.path.basename(abs_file_path)}"'

    if not os.path.exists(os.path.dirname(abs_file_path)):
        os.makedirs(os.path.dirname(abs_file_path))

    with open(abs_file_path, "w") as file:
        if file is None:
            return f'Error: Could not open file: "{os.path.basename(abs_file_path)}"'
        chars_written = file.write(content)

    if 0 >= chars_written:
        return f'Error: Unable to write to file: "{os.path.basename(abs_file_path)}"'

    return f'Successfully wrote to file "{abs_file_path}" ({chars_written} characters written)'