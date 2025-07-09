# get_files_info.py

import os
from google.genai import types

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)

def get_file_metadata(path: str) -> str:
    file_name = os.path.basename(path)
    file_size = os.path.getsize(path)
    is_dir = os.path.isdir(path)
    return f"- {file_name}: file_size={file_size} bytes, is_dir={is_dir}"

def get_files_info(working_directory: str, directory: None|str = None) -> str:
    working_directory_path = os.path.abspath(working_directory)
    directory_path = os.path.abspath(os.path.join(working_directory, directory))

    if not directory_path.startswith(working_directory_path):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    if not os.path.exists(directory_path) or not os.path.isdir(directory_path):
        return f'Error: "{os.path.basename(directory_path)}" is not a directory'

    file_names = os.listdir(directory_path)
    if len(file_names) == 0:
        return f'Error: "{os.path.basename(directory_path)}" is empty'


    directory_content = []
    for file in file_names:
        file_path = os.path.join(directory_path, file)
        if os.path.exists(file_path):
            directory_content.append(get_file_metadata(file_path))

    return "\n".join(directory_content)
