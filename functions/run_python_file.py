# run_python_file.py

import os
import subprocess

def run_python_file(working_directory: str, file_name: str) -> str:
    working_directory_path = os.path.abspath(working_directory)
    file_path = os.path.abspath(os.path.join(working_directory, file_name))
    if not file_path.startswith(working_directory_path):
        return f'Error: Cannot execute "{file_name}" as it is outside the permitted working directory'
    if not os.path.exists(file_path):
        return f'Error: File "{os.path.basename(file_path)}" not found'
    if not os.path.isfile(file_path) or not file_path[-3:] == ".py":
        return f'Error: File not found or is not a Python file: "{file_name}"'

    try:
        process = subprocess.run(["python3", file_path], capture_output=True, timeout=30, cwd=working_directory_path)
    except Exception as e:
        return f"Error: executing Python file: {e}"

    output = "STDOUT: " + str(process.stdout)
    output += "\nSTDERR: " + str(process.stderr)
    if (process.stderr is None) and (process.stdout is None):
        output += "\nNo output produced."
    if process.returncode != 0:
        output += "\nProcess exited with code " + process.returncode

    return output