import os

from functions.exceptions import OutsideWorkDirException
from functions.utils import validate_new_file_path


def write_file(working_directory: str, file_path: str, content: str):
    error_template = "Error: {error}"
    error_message = ""
    try:
        absolute_filepath = validate_new_file_path(working_directory, file_path)
        dir_path = os.path.dirname(absolute_filepath)
        os.makedirs(dir_path, exist_ok=True)
        with open(absolute_filepath, "w") as f:
            f.write(content)

    except OutsideWorkDirException:
        error_message = (
            f'Cannot write to "{file_path}" as it is outside '
            "the permitted working directory"
        )
    except Exception as e:
        error_message = str(e)
    finally:
        if error_message:
            return error_template.format(error=error_message)
    return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
