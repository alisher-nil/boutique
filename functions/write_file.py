from functions.config import ERROR_TEMPLATE
from functions.exceptions import OutsideWorkDirException
from functions.utils import (
    create_directory_if_missing,
    resolve_file_path,
)
from functions.validators import path_within_bounds


def write_file(working_directory: str, file_path: str, content: str):
    try:
        full_file_path = validate_file_path(working_directory, file_path)
        create_directory_if_missing(full_file_path)
        with open(full_file_path, "w") as output_file:
            output_file.write(content)
    except Exception as e:
        return ERROR_TEMPLATE.format(error=e)

    return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'


def validate_file_path(working_directory: str, file_path: str) -> str:
    full_file_path = resolve_file_path(working_directory, file_path)
    working_directory_path = resolve_file_path(working_directory)
    try:
        path_within_bounds(full_file_path, working_directory_path)
    except OutsideWorkDirException:
        raise Exception(
            f'Cannot write to "{file_path}" as it is outside '
            "the permitted working directory"
        )
    return full_file_path
