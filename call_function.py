from google.genai import types
from config import WORKING_DIRECTORY
from functions.get_file_content import get_file_content
from functions.get_files_info import get_files_info
from functions.overwrite_file import overwrite_file
from functions.run_python import run_python_file

funcs = {
    "get_file_content": get_file_content,
    "get_files_info": get_files_info,
    "overwrite_file": overwrite_file,
    "run_python_file": run_python_file
}

def call_function(call: types.FunctionCall, verbose: bool=False) -> types.Content:
    if verbose:
        print(f" - Calling function: {call.name}({call.args})")
    else:
        print(f" - Calling function: {call.name}")

    if call.name not in funcs:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=call.name,
                    response={"error": f"Unknown function {call.name}"}
                )
            ],
        )

    call.args["working_directory"] = WORKING_DIRECTORY
    res = funcs[call.name](**call.args)
    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=call.name,
                response={"output": res}
            )
        ]
    )
    