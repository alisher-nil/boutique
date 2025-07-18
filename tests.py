from functions.get_file_content import get_file_content
from functions.get_files_info import get_files_info
from functions.run_python_file import run_python_file
from functions.write_file import write_file


def test_functions() -> None:
    print(f"Result for current directory: \n{get_files_info(directory='.')}")
    # print(
    #     f"Result for 'pkg' directory: \n{get_files_info('calculator', 'pkg')}"
    # )
    # print(
    #     f"Result for '/bin' directory: \n{get_files_info('calculator', '/bin')}"
    # )
    # print(
    #     f"Result for '../' directory: \n{get_files_info('calculator', '../')}"
    # )


def test_content() -> None:
    print(get_file_content("calculator", "main.py"))
    print(get_file_content("calculator", "pkg/calculator.py"))
    print(get_file_content("calculator", "/bin/cat"))


def test_write_content():
    print(
        write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum")
    )
    print(
        write_file(
            "calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet"
        )
    )
    print(
        write_file("calculator", "/tmp/temp.txt", "this should not be allowed")
    )


def test_execution():
    # should print the calculator's usage instructions)
    print(run_python_file("calculator", "main.py"))
    # should run the calculator... which gives a kinda nasty rendered result
    print(run_python_file("calculator", "main.py", ["3 + 5"]))
    print(run_python_file("calculator", "tests.py"))
    # this should return an error
    print(run_python_file("calculator", "../main.py"))
    # this should return an error
    print(run_python_file("calculator", "nonexistent.py"))


if __name__ == "__main__":
    # test_content()
    test_functions()
    # test_write_content()
    # test_execution()
