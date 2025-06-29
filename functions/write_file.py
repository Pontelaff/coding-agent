# write_file.py

import os

def write_file(working_directory: str, file_name: str, content: str) -> str:
    working_directory_path = os.path.abspath(working_directory)
    file_path = os.path.abspath(os.path.join(working_directory, file_name))

    if not file_path.startswith(working_directory_path):
        return f'Error: Cannot write to "{os.path.basename(file_path)}" as it is outside the permitted working directory'
    if os.path.exists(file_path) and not os.path.isfile(file_path):
        return f'Error: File is not a regular file: "{os.path.basename(file_path)}"'

    if not os.path.exists(os.path.dirname(file_path)):
        os.makedirs(os.path.dirname(file_path))

    with open(file_path, "w") as file:
        if file is None:
            return f'Error: Could not open file: "{os.path.basename(file_path)}"'
        chars_written = file.write(content)

    if 0 >= chars_written:
        return f'Error: Unable to write to file: "{os.path.basename(file_path)}"'

    return f'Successfully wrote to file "{file_path}" ({chars_written} characters written)'