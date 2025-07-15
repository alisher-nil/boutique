import os

from functions.exceptions import NotAPythonFile, OutsideWorkDirException


def verify_filepath_is_valid_and_exists(working_directory: str, file_path: str) -> str:
    valid_path = verify_filepath_is_valid(working_directory, file_path)
    check_file_existence(valid_path)
    return valid_path


def verify_filepath_is_valid(working_directory: str, file_path: str) -> str:
    absolute_filepath = os.path.abspath(os.path.join(working_directory, file_path))
    absolute_directory = os.path.abspath(working_directory)
    check_file_within_directory(absolute_filepath, absolute_directory)
    return absolute_filepath


def check_file_within_directory(file_path: str, working_directory: str) -> None:
    if not file_path.startswith(os.path.abspath(working_directory)):
        raise OutsideWorkDirException


def check_file_existence(file_path: str) -> None:
    if not os.path.exists(file_path) or not os.path.isfile(file_path):
        raise FileNotFoundError


def ensure_directory_exists(file_path: str) -> None:
    dir_path = os.path.dirname(file_path)
    os.makedirs(dir_path, exist_ok=True)


def validate_directory(working_directory: str, directory: str | None) -> str:
    directory = "" if directory is None else directory
    absolute_directory_path = os.path.abspath(
        os.path.join(working_directory, directory)
    )
    if not absolute_directory_path.startswith(os.path.abspath(working_directory)):
        raise ValueError(
            f'Cannot list "{directory}" as it'
            " is outside the permitted working directory"
        )
    if not os.path.isdir(absolute_directory_path):
        raise ValueError(f'"{os.path.basename(directory)}" is not a directory')

    return absolute_directory_path


def check_if_python_file(file_path: str) -> None:
    if not file_path.endswith(".py"):
        raise NotAPythonFile
