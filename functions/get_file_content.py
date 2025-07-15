from functions.config import MAX_CHARS
from functions.exceptions import OutsideWorkDirException
from functions.utils import verify_filepath_is_valid_and_exists


def get_file_content(working_directory: str, file_path: str) -> str:
    error_template = "Error: {error}"
    error_message = ""
    try:
        absolute_filepath = verify_filepath_is_valid_and_exists(
            working_directory,
            file_path,
        )
        with open(absolute_filepath, "r") as f:
            file_content = f.read(MAX_CHARS)
            # checking is there's anything after the limit:
            content_partial = len(f.read(1)) == 1
            if content_partial:
                file_content += (
                    f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
                )

    except FileNotFoundError:
        error_message = f'File not found or is not a regular file: "{file_path}"'
    except OutsideWorkDirException:
        error_message = (
            f'Cannot read "{file_path}" as it is '
            "outside the permitted working directory"
        )
    except Exception as e:
        error_message = str(e)
    finally:
        if error_message:
            return error_template.format(error=error_message)

    return file_content
