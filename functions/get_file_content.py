import os

from functions.config import MAX_CHARS


def validate_file_path(working_directory, file_path):
    absolute_filepath = os.path.abspath(os.path.join(working_directory, file_path))
    if not absolute_filepath.startswith(os.path.abspath(working_directory)):
        raise ValueError(
            f'Cannot read "{file_path}" as it is '
            "outside the permitted working directory"
        )
    if not os.path.exists(absolute_filepath) or not os.path.isfile(absolute_filepath):
        raise ValueError(f'File not found or is not a regular file: "{file_path}"')
    return absolute_filepath


def get_file_content(working_directory, file_path):
    try:
        absolute_filepath = validate_file_path(working_directory, file_path)
        with open(absolute_filepath, "r") as f:
            file_content = f.read(MAX_CHARS)
            content_partial = len(f.read(1)) == 1
            if content_partial:
                file_content += f'[...File "{file_path}" truncated at 10000 characters]'
    except Exception as e:
        return f"Error: {e}"

    return file_content
