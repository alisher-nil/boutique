from functions.config import ERROR_TEMPLATE
from functions.exceptions import NotAPythonFile, OutsideWorkDirException
from functions.utils import resolve_file_path
from functions.validators import (
    file_exists,
    file_is_python,
    path_within_bounds,
)


def run_python_file(working_directory: str, file_path: str, args: list = []):
    try:
        full_file_path = validate_file_path(working_directory, file_path)
    except Exception as e:
        return ERROR_TEMPLATE.format(error=str(e))


def validate_file_path(working_directory: str, file_path: str):
    full_file_path = resolve_file_path(working_directory, file_path)
    working_directory_path = resolve_file_path(working_directory)
    try:
        path_within_bounds(full_file_path, working_directory_path)
        file_exists(full_file_path)
        file_is_python(full_file_path)
    except OutsideWorkDirException:
        raise Exception(
            f'Cannot execute "{file_path}" as it is '
            "outside the permitted working directory"
        )
    except FileNotFoundError:
        raise Exception(f'File "{file_path}" not found.')
    except NotAPythonFile:
        raise Exception(f'"{file_path}" is not a Python file.')
    return full_file_path
