import os

from functions.exceptions import OutsideWorkDirException


def validate_exsisting_file_path(working_directory: str, file_path: str) -> str:
    absolute_filepath = os.path.abspath(os.path.join(working_directory, file_path))
    absolute_directory = os.path.abspath(working_directory)
    validate_file_in_workdir(absolute_filepath, absolute_directory)
    validate_file_exists(absolute_filepath)
    return absolute_filepath


def validate_new_file_path(working_directory: str, file_path: str) -> str:
    absolute_filepath = os.path.abspath(os.path.join(working_directory, file_path))
    absolute_directory = os.path.abspath(working_directory)
    validate_file_in_workdir(absolute_filepath, absolute_directory)
    return absolute_filepath


def validate_file_in_workdir(file_path, working_directory):
    if not file_path.startswith(os.path.abspath(working_directory)):
        raise OutsideWorkDirException


def validate_file_exists(file_path):
    if not os.path.exists(file_path) or not os.path.isfile(file_path):
        raise FileNotFoundError
