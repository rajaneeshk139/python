"""
test of the module string_to_lisp
"""
import unittest
import subprocess

import general_utilities as gu
import string_to_lisp as stc
import base_string_to_code_test


def get_lisp_interpreter():
    """returns the name of the lisp interpreter"""
    return 'clisp'


def run_lisp_code(in_code):
    """
    Runs the lisp code in_code.
    Returns the output of the program.
    """
    source_filename = gu.get_unique_filename('lsp')
    gu.save_str_to_file(
        gu.get_tmp_test_folder_path()/source_filename, in_code)
    res = subprocess.run(
        [get_lisp_interpreter(), source_filename],
        cwd=str(gu.get_tmp_test_folder_path()),
        check=True,
        capture_output=True,
        text=True)
    if len(res.stdout) > 1:
        assert res.stdout[-1] == '\n'
        res.stdout = res.stdout[0:-1]
    return res


class TestSetup(unittest.TestCase):
    """
    tests verifying if the setup of the system is suitable
    to perform other tests
    """
    def test_compiler(self):
        gu.check_version(get_lisp_interpreter())


class TestStringToLisp(base_string_to_code_test.BaseStringToCode):
    """
    unit tests for the function string_to_lisp.proc
    """
    __test__ = True

    def str_to_code(_, in_str):
        return stc.proc(in_str)

    def run_code(_, in_code):
        return run_lisp_code(in_code)


if __name__ == '__main__':
    unittest.main()
