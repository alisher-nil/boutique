from functions.config import ERROR_TEMPLATE, MAX_CHARS
from functions.exceptions import OutsideWorkDirException
from functions.utils import resolve_file_path
from functions.validators import file_exists, path_within_bounds


def get_file_content(working_directory: str, file_path: str) -> str:
    try:
        resolved_file_path = validate_file_path(working_directory, file_path)
        file_content = read_content(resolved_file_path)
    except Exception as e:
        return ERROR_TEMPLATE.format(error=e)

    return file_content


def read_content(file_path: str) -> str:
    with open(file_path, "r") as f:
        file_content = f.read(MAX_CHARS)

        # checking is there's anything left after the limit:
        content_partial = len(f.read(1)) == 1
        # if so, we append a message about truncation to the end of the content
        if content_partial:
            truncation_message = (
                f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
            )
            file_content += truncation_message
    return file_content


def validate_file_path(working_directory: str, file_path: str) -> str:
    abs_file_path = resolve_file_path(working_directory, file_path)
    abs_working_directory = resolve_file_path(working_directory)
    try:
        path_within_bounds(abs_file_path, abs_working_directory)
        file_exists(abs_file_path)
    except OutsideWorkDirException:
        raise ValueError(
            f'Cannot read "{file_path}" as it is '
            "outside the permitted working directory"
        )
    except FileNotFoundError:
        raise ValueError(
            f'File not found or is not a regular file: "{file_path}"'
        )
    return abs_file_path
