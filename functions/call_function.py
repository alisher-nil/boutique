from typing import Callable

from google.genai import types

from functions.get_file_content import get_file_content
from functions.get_files_info import get_files_info
from functions.run_python_file import run_python_file
from functions.write_file import write_file

name_func_map: dict[str, Callable] = {
    "get_file_content": get_file_content,
    "get_files_info": get_files_info,
    "run_python_file": run_python_file,
    "write_file": write_file,
}


def call_function(function_call_part, verbose: bool = False) -> types.Content:
    func_name: str = function_call_part.name
    func_args: str = function_call_part.args

    if verbose:
        print(f"Calling function: {func_name}({func_args})")
    else:
        print(f" - Calling function: {func_name}")
    work_dir: str = "./calculator"
    if func_name in name_func_map:
        func = name_func_map[func_name]
        func_result = func(**func_args, working_directory=work_dir)
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=func_name,
                    response={"result": func_result},
                )
            ],
        )

    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=func_name,
                response={"error": f"Unknown function: {func_name}"},
            )
        ],
    )
