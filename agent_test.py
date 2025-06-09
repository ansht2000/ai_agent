from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.overwrite_file import overwrite_file
from functions.run_python import run_python_file
import re

class TestGetFilesInfo:
    def test_calculator_dir(self):
        calc_list = get_files_info("calculator", ".")
        assert "- pkg: file_size=0 bytes, is_dir=True" in calc_list
        assert "- __pycache__: file_size=0 bytes, is_dir=True" in calc_list
        assert re.search(r"- calc_test.py: file_size=\d+ bytes, is_dir=False", calc_list)
        assert re.search(r"- main.py: file_size=\d+ bytes, is_dir=False", calc_list)

    def test_pkg_dir(self):
        pkg_list = get_files_info("calculator", "pkg")
        assert "- __pycache__: file_size=0 bytes, is_dir=True" in pkg_list
        assert re.search(r"- calculator.py: file_size=\d+ bytes, is_dir=False", pkg_list)
        assert re.search(r"- render.py: file_size=\d+ bytes, is_dir=False", pkg_list)

    def test_bin_dir(self):
        bin_list = get_files_info("calculator", "/bin")
        assert re.search(r"^Error: Cannot list '[./-_a-zA-Z0-9]+' as it is outside the permitted working directory$", bin_list)

    def test_parent_dir(self):
        prev_dir_list = get_files_info("calculator", "../")
        assert re.search(r"^Error: Cannot list '[./-_a-zA-Z0-9]+' as it is outside the permitted working directory$", prev_dir_list)

class TestGetFilesContent:
    def test_main_py(self):
        main_text = get_file_content("calculator", "main.py")
        assert re.search(r"^# main.py", main_text)

    def test_calc_py(self):
        pkg_calc_text = get_file_content("calculator", "pkg/calculator.py")
        assert re.search(r"^# calculator.py", pkg_calc_text)

    def test_bin_cat(self):
        err_text = get_file_content("calculator", "/bin/cat")
        assert re.search(r"^Error: Cannot read '[./-_a-zA-Z0-9]+' as it is outside the permitted working directory$", err_text)

class TestOverwriteFile:
    def test_lorem_file(self):
        lorem_text = overwrite_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum")
        assert re.search(r"^Successfully wrote to '[./-_a-zA-Z0-9]+' \(\d+ bytes written\)$", lorem_text)

    def test_pkg_lorem_file(self):
        pkg_lorem_text = overwrite_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet")
        assert re.search(r"^Successfully wrote to '[./-_a-zA-Z0-9]+' \(\d+ bytes written\)$", pkg_lorem_text)

    def test_tmp_text(self):
        error_text = overwrite_file("calculator", "/tmp/temp/txt", "this should not be allowed")
        assert re.search(r"Error: Cannot write to '[./-_a-zA-Z0-9]+' as it is outside the permitted working directory", error_text)

class TestRunPython:
    def test_main_py(self):
        out = run_python_file("calculator", "main.py")
        assert "STDOUT" in out and "STDERR" in out

    def test_tests_py(self):
        out = run_python_file("calculator", "tests.py")
        assert "STDOUT" in out and "STDERR" in out

    def test_outside_main_py(self):
        out = run_python_file("calculator", "../main.py")
        assert "Error" in out

    def test_outside_nonexistent_py(self):
        out = run_python_file("calculator", "nonexistent.py")
        assert "Error" in out

    