import pytest
import itertools
import general_utilities as gu

import setup_bash
import setup_cpp
import setup_python
import setup_lisp


def check_output(in_ex_output, in_target_str):
    """
    does all of the checks of the program output against the expected
    result
    """
    assert in_ex_output.stdout == in_target_str
    assert not in_ex_output.stderr


def get_all_test_data():
    return (_.get_test_data()
            for _ in [setup_cpp, setup_bash, setup_python, setup_lisp])


def get_all_function_pairs():
    return ((_.string_to_code, _.run_code) for _ in get_all_test_data())


def get_all_ids():
    return (_.id for _ in get_all_test_data())


def get_all_tool_names():
    return itertools.chain(*(_.tool_names for _ in get_all_test_data()))


@pytest.mark.parametrize('tool_name', get_all_tool_names())
def test_tool(tool_name):
    gu.check_version(tool_name)

@pytest.fixture(
    params=get_all_function_pairs(), ids=get_all_ids())
def fun_pair(request):
    yield request.param


@pytest.fixture(params=[
    'Hello World!',
    'a',
    '\n',
    ' ',
    ';'
    '\\',
    '\n'.join(['Line 1', 'Line 2']),
    '',
    '#',
    'aaa\tb\nccc\t#',
    '\'',
    '\"',
    '~',
    '{',
    '`'])
def example_string(request):
    yield request.param


def test_string_to_code(tmp_path, fun_pair, example_string):
    """
    basic test of the string_to_code type function
    """
    str_to_code_fun, run_code_fun = fun_pair
    source_code = str_to_code_fun(example_string)
    executable_output = run_code_fun(source_code, tmp_path)
    check_output(executable_output, example_string)


def test_string_to_code_iteration(tmp_path, fun_pair, example_string):
    """
    tests the iterations of the string_to_code function
    """
    str_to_code_fun, run_code_fun = fun_pair
    string_list = [example_string]
    max_iteration = 2
    for _ in range(max_iteration):
        string_list.append(str_to_code_fun(string_list[-1]))

    for _ in range(max_iteration, 0, -1):
        check_output(run_code_fun(string_list[_], tmp_path), string_list[_-1])