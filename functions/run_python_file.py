# run_python_file.py

import os
import subprocess
from google.genai import types

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Execute a specified Python file, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path to execute, relative to the working directory.",
            ),
        },
    ),
)

def run_python_file(working_directory: str, file_path: str) -> str:
    working_directory_path = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))
    if not abs_file_path.startswith(working_directory_path):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    if not os.path.exists(abs_file_path):
        return f'Error: File "{os.path.basename(abs_file_path)}" not found'
    if not os.path.isfile(abs_file_path) or not abs_file_path[-3:] == ".py":
        return f'Error: File not found or is not a Python file: "{file_path}"'

    try:
        process = subprocess.run(["python3", abs_file_path], capture_output=True, timeout=30, cwd=working_directory_path)
    except Exception as e:
        return f"Error: executing Python file: {e}"

    output = "STDOUT: " + str(process.stdout)
    output += "\nSTDERR: " + str(process.stderr)
    if (process.stderr is None) and (process.stdout is None):
        output += "\nNo output produced."
    if process.returncode != 0:
        output += "\nProcess exited with code " + process.returncode

    return output