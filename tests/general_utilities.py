"""
general utilities for tests
"""
import collections
import pathlib
import sys
import subprocess

Language = collections.namedtuple(
    'Language', ['tool_names', 'string_to_code', 'run_code', 'id'])


def project_folder():
    """returns the path of the main folder of this project"""
    this_file_path = pathlib.Path(__file__)
    for _ in this_file_path.parents:
        if _.name == 'string_to_code_proj':
            res = _
            break
    else:
        raise RuntimeError('Wrong folder structure')
    return res.resolve()


sys.path.insert(0, str(project_folder()))


def save_str_to_file(in_file_path, in_str):
    """writes in_str into the file in_file_path"""
    with open(in_file_path, mode='x', encoding='utf-8') as output_file:
        output_file.write(in_str)


def get_unique_filename(in_tmp_folder, in_file_extension):
    """
    returns a file name with in_file_extension,
    which does not exist in the folder get_tmp_test_folder_path()
    """
    def gen_names():
        cur_try_num = 0
        while True:
            yield f'tmp_file_{cur_try_num}.'+in_file_extension
            cur_try_num += 1
    for _ in gen_names():
        if not (in_tmp_folder/_).exists():
            return _


def check_version(in_program_name):
    """
    Checks the version of the given program.
    Useful when checking if a given program is present in the system.
    """
    subprocess.run(
        [in_program_name, '--version'],
        check=True,
        capture_output=True)
