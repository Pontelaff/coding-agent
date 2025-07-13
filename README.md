# AI Coding Agent

This agent uses the Google GenAI API to assist with development tasks by allowing it to read, write, and execute files within a specified working directory.

## Usage

1.  Set the `GEMINI_API_KEY` environment variable with your Google Gemini API key.
2.  Run the `main.py` script with the working directory and prompt as arguments:

    ```bash
    python main.py <working_dir> "<PROMPT>" [--verbose]
    ```

    *   `<working_dir>`: The working directory for the agent. All file paths in the prompt should be relative to this directory.
    *   `<PROMPT>`: The task you want the agent to perform.  Enclose the prompt in quotation marks.
    *   `--verbose`: (Optional) Enables verbose output, showing the function calls and responses.

    Example:

    ```bash
    python main.py ../src "Fix formatting in print_info() in file pkg/data_reader.py" --verbose
    ```

ATTENTION: This tool can access and manipulate any files within the specified working directory. Set it carefully to avoid accidentally overwriting important files.

## Available Functions

The agent can use the following functions:

*   `get_files_info(directory: str)`: Lists files and directories within the working directory.
*   `get_file_content(file_path: str)`: Reads the content of a file within the working directory.
*   `write_file(file_path: str, content: str)`: Writes or overwrites a file within the working directory.
*   `run_python_file(file_path: str)`: Executes a Python file within the working directory.

All paths provided to these functions must be relative to the working directory.
