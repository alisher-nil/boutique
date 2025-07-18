from google.genai import types

from functions.exceptions import OutsideWorkDirException
from functions.utils import (
    extract_file_info,
    get_folder_content,
    resolve_file_path,
)
from functions.validators import directory_exists, path_within_bounds


def get_files_info(directory: str = ".") -> str:
    working_directory: str = "calculator"
    try:
        target_dir_path = validate_directory_path(working_directory, directory)
        absolute_file_paths = get_folder_content(target_dir_path)
        collected_file_info = map(extract_file_info, absolute_file_paths)

    except Exception as e:
        return f"Error: {e}"

    return "\n".join(collected_file_info)


def validate_directory_path(working_directory: str, directory: str) -> str:
    target_dir_path = resolve_file_path(working_directory, directory)
    working_directory_path = resolve_file_path(working_directory)
    try:
        path_within_bounds(target_dir_path, working_directory_path)
        directory_exists(target_dir_path)
    except OutsideWorkDirException:
        raise Exception(
            f'Cannot list "{directory}" as it is outside'
            " the permitted working directory"
        )
    except FileNotFoundError:
        raise Exception(f'"{directory}" is not a directory')

    return target_dir_path


schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their "
    "sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the "
                "working directory. If not provided, lists files in the "
                "working directory itself.",
            ),
        },
    ),
)
