from functions.common import ERROR_TEMPLATE
from functions.exceptions import OutsideWorkDirException
from functions.utils import (
    create_directory_if_missing,
    verify_filepath_is_valid,
)


def write_file(working_directory: str, file_path: str, content: str):
    error_message = ""
    try:
        full_file_path = verify_filepath_is_valid(working_directory, file_path)
        create_directory_if_missing(full_file_path)
        with open(full_file_path, "w") as output_file:
            output_file.write(content)

    except OutsideWorkDirException:
        error_message = (
            f'Cannot write to "{file_path}" as it is outside '
            "the permitted working directory"
        )
    except Exception as e:
        error_message = str(e)
    finally:
        if error_message:
            return ERROR_TEMPLATE.format(error=error_message)
    return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
