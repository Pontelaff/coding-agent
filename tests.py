#!/usr/bin/env python3

from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content

def test_get_files_info():
    print(get_files_info("../calculator", "."))
    print(get_files_info("../calculator", "pkg"))
    print(get_files_info("../calculator", "bin"))
    print(get_files_info("../calculator", "empty"))
    print(get_files_info("../calculator", ".."))

def test_get_file_content():
    print(get_file_content("../calculator", "main.py"))
    print(get_file_content("../calculator", "pkg/calculator.py"))
    print(get_file_content("../calculator", "/bin/cat"))

def main() -> None:
    #test_get_files_info()
    test_get_file_content()

if __name__ == "__main__":
    main()