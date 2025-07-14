import os
from functools import partial


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


def get_file_info(filename: str) -> str:
    info_template = "- {filename}: file_size={filesize} bytes, is_dir={is_dir}"
    return info_template.format(
        filename=os.path.basename(filename),
        filesize=os.path.getsize(filename),
        is_dir=os.path.isdir(filename),
    )


def get_files_info(working_directory: str, directory: str | None = None) -> str:
    try:
        absolute_directory_path = validate_directory(working_directory, directory)

        directory_files = os.listdir(absolute_directory_path)
        full_path_builder = partial(os.path.join, absolute_directory_path)
        absolute_file_paths = map(full_path_builder, directory_files)

        collected_file_info = map(get_file_info, absolute_file_paths)

    except Exception as e:
        return f"Error: {e}"

    return "\n".join(collected_file_info)
