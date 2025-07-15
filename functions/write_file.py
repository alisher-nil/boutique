from functions.utils import validate_file_path


def write_file(working_directory: str, file_path: str, content: str):
    try:
        absolute_filepath = validate_file_path(working_directory, file_path)
    except Exception as e:
        return f"Error: {e}"
