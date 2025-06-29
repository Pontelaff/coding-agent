# get_file_content.py

import os

MAX_CHARACTERS = 10000

def get_file_content(working_directory: str, file_name: str) -> str:
    working_directory_path = os.path.abspath(working_directory)
    file_path = os.path.abspath(os.path.join(working_directory, file_name))
    if not file_path.startswith(working_directory_path):
        return f'Error: Cannot read "{os.path.basename(file_path)}" as it is outside the permitted working directory'
    if not os.path.exists(file_path) or not os.path.isfile(file_path):
        return f'Error: File not found or is not a regular file: "{os.path.basename(file_path)}"'

    with open(file_path, "r") as file:
        if file is None:
            return f'Error: could not read file: "{os.path.basename(file_path)}"'
        file_content = file.read(MAX_CHARACTERS)

    if os.path.getsize(file_path) > MAX_CHARACTERS:
        file_content += f'[...File "{os.path.basename(file_path)}" truncated at 10000 characters]'

    return file_content