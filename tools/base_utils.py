import re
import pyperclip


def replace_mass(text, patterns, replaced):
    for pattern in patterns:
        text = re.sub(pattern, replaced, text)
    return text


def find(predicate, items):
    return next((item for item in items if predicate(item)), None)


def copy_to_clipboard(data):
    pyperclip.copy(data)


def paste_from_clopboard():
    return pyperclip.paste()
