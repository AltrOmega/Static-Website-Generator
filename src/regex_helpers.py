import re
from typing import Tuple, Pattern


def str_to_regex(str_: str) -> Pattern:
    split = str_.split('%')
    split_iter = map(lambda x: re.escape(x), split)
    regex = '(.*?)'.join(split_iter)
    return re.compile(regex, re.DOTALL)

def strings_to_regexes(*strings) -> Tuple[Pattern]:
    return tuple(map(lambda x: str_to_regex(x), strings))



def str_begin_to_regex(str_: str) -> Pattern:
    split = str_.split('%')
    split_iter = map(lambda x: re.escape(x), split)
    regex = f"^{'(.*?)'.join(split_iter)}$"
    return re.compile(regex)

def strings_begin_to_regexes(*strings) -> Tuple[Pattern]:
    return tuple(map(lambda x: str_begin_to_regex(x), strings))