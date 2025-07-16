import os

from functions.exceptions import NotAPythonFile, OutsideWorkDirException


def path_within_bounds(target_path: str, parent_path: str) -> str:
    """
    Check if the target path is within the bounds of the parent path.
    Raises:
        OutsideWorkDirException: If the target path is outside the parent path.
    """
    if not target_path.startswith(os.path.abspath(parent_path)):
        raise OutsideWorkDirException
    return target_path


def file_exists(target_path: str) -> str:
    """
    Check if the target file exists and is a file.
    Raises:
        FileNotFoundError: If the target file does not exist or is not a file.
    """
    if not os.path.exists(target_path):
        raise FileNotFoundError("File does not exist")
    if not os.path.isfile(target_path):
        raise FileNotFoundError("File is not a valid file")
    return target_path


def directory_exists(target_path: str) -> str:
    """
    Check if the target directory exists.
    Raises:
        FileNotFoundError: If the target directory does not exist.
    """
    if not os.path.exists(target_path):
        raise FileNotFoundError("Directory does not exist")
    if not os.path.isdir(target_path):
        raise FileNotFoundError("Path is not a valid directory")
    return target_path


def file_is_python(file_path: str) -> str:
    """
    Check if the file is a Python file.
    Raises:
        NotAPythonFile: If the file is not a Python file.
    """
    if not file_path.endswith(".py"):
        raise NotAPythonFile("File is not a Python file")
    return file_path
