from functions.get_file_content import get_file_content
from functions.get_files_info import get_files_info


def test_functions() -> None:
    print(f"Result for current directory: \n{get_files_info('calculator', '.')}")
    print(f"Result for 'pkg' directory: \n{get_files_info('calculator', 'pkg')}")
    print(f"Result for '/bin' directory: \n{get_files_info('calculator', '/bin')}")
    print(f"Result for '../' directory: \n{get_files_info('calculator', '../')}")


def test_content() -> None:
    print(get_file_content("calculator", "main.py"))
    print(get_file_content("calculator", "pkg/calculator.py"))
    print(get_file_content("calculator", "/bin/cat"))


if __name__ == "__main__":
    test_content()
    # test_functions()
