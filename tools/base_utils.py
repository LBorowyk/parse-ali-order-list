import re
import pyperclip


def replace_mass(text, patterns, replaced):
    for pattern in patterns:
        text = re.sub(pattern, replaced, text)
    return text


def clear_number_str(s):
    return re.sub(r'[^0-9\.-]', '', s)


def to_float(s):
    return float(clear_number_str(s))


def to_int(s):
    return int(clear_number_str(s))


def find(predicate, items):
    return next((item for item in items if predicate(item)), None)


def copy_to_clipboard(data):
    pyperclip.copy(data)


def paste_from_clopboard():
    return pyperclip.paste()
