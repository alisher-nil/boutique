from functions.config import ERROR_TEMPLATE
from functions.exceptions import OutsideWorkDirException
from functions.utils import read_content, resolve_file_path
from functions.validators import file_exists, path_within_bounds


def get_file_content(working_directory: str, file_path: str) -> str:
    try:
        resolved_file_path = validate_file_path(working_directory, file_path)
        file_content = read_content(resolved_file_path)
    except Exception as e:
        return ERROR_TEMPLATE.format(error=e)

    return file_content


def validate_file_path(working_directory: str, file_path: str) -> str:
    abs_file_path = resolve_file_path(working_directory, file_path)
    abs_working_directory = resolve_file_path(working_directory)
    try:
        path_within_bounds(abs_file_path, abs_working_directory)
        file_exists(abs_file_path)
    except OutsideWorkDirException:
        raise Exception(
            f'Cannot read "{file_path}" as it is '
            "outside the permitted working directory"
        )
    except FileNotFoundError:
        raise Exception(
            f'File not found or is not a regular file: "{file_path}"'
        )
    return abs_file_path
