# call_function.py

from google.genai import types

from config import WORKING_DIR
from functions.get_files_info import get_files_info, schema_get_files_info
from functions.get_file_content import get_file_content, schema_get_file_content
from functions.write_file import write_file, schema_write_file
from functions.run_python_file import run_python_file, schema_run_python_file

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_write_file,
        schema_run_python_file,
    ]
)


def execute_function_calls(function_calls: types.FunctionCall, verbose: bool) -> list[types.Content]:
    function_responses = []
    for call in function_calls:
        function_call_result = call_function(call, verbose)
        if not function_call_result.parts or not function_call_result.parts[0].function_response:
            raise RuntimeError(f'ERROR: Empty function call result: "{call.name}"')
        elif verbose:
            print(f"-> {function_call_result.parts[0].function_response.response}")
        function_responses.append(function_call_result)

    if not function_responses:
        raise RuntimeError(f'ERROR: Failed to get function responses')

    return function_responses

def call_function(function_call_part: types.FunctionCall, verbose=False) -> types.Content:
    functions = {
        "get_files_info" : get_files_info,
        "get_file_content" : get_file_content,
        "write_file" : write_file,
        "run_python_file" : run_python_file,
    }
    function_name = function_call_part.name
    function_args = function_call_part.args
    if verbose:
        print(f"Calling function: {function_name}({function_args})")
    else:
        print(f"Calling function: {function_name}")

    func = functions[function_name]
    try:
        function_result = func(working_directory=WORKING_DIR, **function_args)
    except NameError:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"},
                )
            ],
        )

    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_name,
                response={"result": function_result},
            )
        ],
    )