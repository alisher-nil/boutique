import subprocess

from functions.config import ERROR_TEMPLATE, SUBPROCESS_TIMEOUT
from functions.exceptions import NotAPythonFile, OutsideWorkDirException
from functions.utils import resolve_file_path
from functions.validators import (
    file_exists,
    file_is_python,
    path_within_bounds,
)

STDOUT_TEMPLATE = "STDOUT: {stdout}"
STDERR_TEMPLATE = "STDERR: {stderr}"


def run_python_file(working_directory: str, file_path: str, args: list = []):
    output = []
    try:
        full_file_path = validate_file_path(working_directory, file_path)
        process = subprocess.run(
            ["python", full_file_path] + args,
            check=True,
            cwd=working_directory,
            timeout=SUBPROCESS_TIMEOUT,
            capture_output=True,
            text=True,
        )
        output.append(STDOUT_TEMPLATE.format(stdout=process.stdout))
        if process.stderr:
            output.append(STDERR_TEMPLATE.format(stderr=process.stderr))
    except subprocess.CalledProcessError as e:
        return f"Process exited with code {e.returncode}"
    except subprocess.SubprocessError as e:
        error_message = f"executing Python file: {e}"
        return ERROR_TEMPLATE.format(error=error_message)
    except Exception as e:
        return ERROR_TEMPLATE.format(error=e)

    if not output:
        output = ["No output produced."]

    return "\n".join(output)


def validate_file_path(working_directory: str, file_path: str):
    full_file_path = resolve_file_path(working_directory, file_path)
    working_directory_path = resolve_file_path(working_directory)
    try:
        path_within_bounds(full_file_path, working_directory_path)
        file_exists(full_file_path)
        file_is_python(full_file_path)
    except OutsideWorkDirException:
        raise Exception(
            f'Cannot execute "{file_path}" as it is '
            "outside the permitted working directory"
        )
    except FileNotFoundError:
        raise Exception(f'File "{file_path}" not found.')
    except NotAPythonFile:
        raise Exception(f'"{file_path}" is not a Python file.')
    return full_file_path
