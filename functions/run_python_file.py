from functions.common import ERROR_TEMPLATE
from functions.exceptions import NotAPythonFile, OutsideWorkDirException
from functions.utils import check_if_python_file, verify_filepath_is_valid_and_exists


def run_python_file(working_directory: str, file_path: str, args: list = []):
    error_message = ""
    try:
        full_path = verify_filepath_is_valid_and_exists(working_directory, file_path)
        check_if_python_file(full_path)
    except OutsideWorkDirException:
        error_message = (
            f'Cannot execute "{file_path}" as it is '
            "outside the permitted working directory"
        )
    except FileNotFoundError:
        error_message = f'File "{file_path}" not found.'
    except NotAPythonFile:
        error_message = f'"{file_path}" is not a Python file.'
    finally:
        if error_message:
            return ERROR_TEMPLATE.format(error_message)
