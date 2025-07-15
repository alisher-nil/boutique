import os

from functions.exceptions import OutsideWorkDirException


def validate_file_path(working_directory: str, file_path: str) -> str:
    absolute_filepath = os.path.abspath(os.path.join(working_directory, file_path))
    if not absolute_filepath.startswith(os.path.abspath(working_directory)):
        raise OutsideWorkDirException
        # raise ValueError(
        #     f'Cannot read "{file_path}" as it is '
        #     "outside the permitted working directory"
        # )
    if not os.path.exists(absolute_filepath) or not os.path.isfile(absolute_filepath):
        raise FileNotFoundError
        # raise ValueError(f'File not found or is not a regular file: "{file_path}"')
    return absolute_filepath
