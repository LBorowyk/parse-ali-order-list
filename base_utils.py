import re
def replace_mass(text, patterns, replaced):
    for pattern in patterns:
        text = re.sub(pattern, replaced, text)
    return text

def find(predicate, items):
    return next((item for item in items if predicate(item)), None)