import os
from functools import partial

from functions.config import FILE_INFO_TEMPLATE, MAX_CHARS
from functions.exceptions import NotAPythonFile, OutsideWorkDirException


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


def get_folder_content(directory: str) -> list[str]:
    files_in_directory = os.listdir(directory)
    full_path_builder = partial(os.path.join, directory)
    absolute_children_paths = map(full_path_builder, files_in_directory)
    return list(absolute_children_paths)


def extract_file_info(filename: str) -> str:
    return FILE_INFO_TEMPLATE.format(
        filename=os.path.basename(filename),
        filesize=os.path.getsize(filename),
        is_dir=os.path.isdir(filename),
    )


def resolve_file_path(
    working_directory: str,
    relative_path: str | None,
) -> str:
    """Resolve the absolute path based on the working directory and relative path.
    If relative_path is None, it defaults to an empty string.
    Args:
        working_directory (str): The base directory to resolve the path against.
        relative_path (str | None): The relative path to resolve.
    Returns:
        str: The absolute target path.
    """
    if relative_path is None:
        relative_path = ""

    absolute_file_path = os.path.abspath(
        os.path.join(
            working_directory,
            relative_path,
        )
    )
    return absolute_file_path


def create_directory_if_missing(file_path: str) -> None:
    dir_path = os.path.dirname(file_path)
    os.makedirs(dir_path, exist_ok=True)


##################################################


# To delete after refactoring
def check_if_python_file(file_path: str) -> None:
    if not file_path.endswith(".py"):
        raise NotAPythonFile


def check_file_existence(file_path: str) -> None:
    if not os.path.exists(file_path) or not os.path.isfile(file_path):
        raise FileNotFoundError


def check_file_within_directory(
    file_path: str, working_directory: str
) -> None:
    if not file_path.startswith(os.path.abspath(working_directory)):
        raise OutsideWorkDirException


def verify_filepath_is_valid_and_exists(
    working_directory: str, file_path: str
) -> str:
    valid_path = verify_filepath_is_valid(working_directory, file_path)
    check_file_existence(valid_path)
    return valid_path


def verify_filepath_is_valid(working_directory: str, file_path: str) -> str:
    absolute_filepath = os.path.abspath(
        os.path.join(working_directory, file_path)
    )
    absolute_directory = os.path.abspath(working_directory)
    check_file_within_directory(absolute_filepath, absolute_directory)
    return absolute_filepath
