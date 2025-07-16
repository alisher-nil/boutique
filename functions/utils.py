import os
from functools import partial

from functions.config import FILE_INFO_TEMPLATE, MAX_CHARS


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
    """
    Create the directory for the given file path if it does not exist.

    Args:
        file_path (str): The path of the file for which the directory
        should be created.
    """
    dir_path = os.path.dirname(file_path)
    os.makedirs(dir_path, exist_ok=True)
