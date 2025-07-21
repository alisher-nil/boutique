from google.genai import types

from .schemas import (
    schema_get_file_content,
    schema_get_files_info,
    schema_run_python_file,
    schema_write_file,
)

available_functions = types.Tool(
    function_declarations=[
        schema_get_file_content,
        schema_get_files_info,
        schema_run_python_file,
        schema_write_file,
    ]
)
