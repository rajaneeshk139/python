"""
provides string_to_python utilities
"""
from . import core


def atom_to_code(in_atom):
    """
    returns a string/piece of python code resulting in printing the
    in_atom.atom_char to the standard output
    """
    assert isinstance(in_atom, core.Atom)
    special_chars = {
        r'"': r'\"',
        r"'": r'\'',
        '\\': '\\\\',
        '\n': '\\n',
        '\t': '\\t'}
    res_char = special_chars.get(in_atom.atom_char, in_atom.atom_char)
    return f'print(\'{res_char}\', end=\'\')'
    assert isinstance(in_atom, core.Atom)


def function_call_str(in_function_name):
    """
    returns a string calling a function with name in_function_name in python
    """
    return f'{in_function_name}()'


def function_to_code(in_function):
    """
    returns a string representing the code of the function definiton in python
    """
    assert isinstance(in_function, core.SimpleFunction)

    def proc_single_body_line(in_line_data):
        if isinstance(in_line_data, core.Atom):
            res = atom_to_code(in_line_data)
        else:
            res = function_call_str(in_line_data.function_name)
        return '    '+res
    function_body = '    pass'
    if in_function.called_list:
        function_body = '\n'.join(
            proc_single_body_line(_) for _ in in_function.called_list)

    return '\n'.join([
        f'def {in_function.function_name}():',
        function_body])


def proc(in_str):
    """
    returns a python code printing in_str to the standard output
    """
    initial_fun, function_stack = core.str_to_function_stack(
        in_str, core.gen_function_names())
    function_list = '\n\n\n'.join(function_to_code(_) for _ in function_stack)
    res = ''
    if initial_fun:
        assert function_stack or isinstance(initial_fun, core.Atom)
        if isinstance(initial_fun, core.Atom):
            assert not function_stack
            main_call = atom_to_code(initial_fun)
        else:
            assert isinstance(initial_fun, core.SimpleFunction)
            main_call = function_call_str(initial_fun.function_name)
        res = main_call+'\n'
        if function_list:
            res = function_list+'\n\n\n'+res
    else:
        assert not function_stack
    return res